"""Provide a Tango gateway server."""

# Imports
import socket
import asyncio
from enum import Enum
from functools import partial
from contextlib import closing

try:
    import prometheus_client
except ImportError:
    prometheus_client = None

# Local imports
from . import giop
from . import zmqforward

# Logging import
import logging
from logging import getLogger, Formatter, StreamHandler


# Create logger
logger = getLogger("Tango gateway")
# Create console handler
log_handler = StreamHandler()
# Create formater
log_format = Formatter('%(levelname)s - %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

# Prometheus monitoring
# If installed, we will use the prometheus_client library to periodically
# export metrics data to a file. If not, this will be ignored.
if prometheus_client:
    prom_registry = prometheus_client.CollectorRegistry()
    prom_counters = {
        "forwarding": prometheus_client.Counter(
            "tango_gateway_forwarding",
            "Forwarded connections",
            ["gw_port", "src_host", "src_port", "dst_host", "dst_port"],
            registry=prom_registry
        ),
        "client_connection": prometheus_client.Counter(
            "tango_gateway_client_connection",
            "Client connection established",
            ["gw_port", "device", "src_host", "src_port", "dst_host", "dst_port"],
            registry=prom_registry
        ),
        "db_client": prometheus_client.Counter(
            "tango_gateway_db_client_connection",
            "Client connections to DB",
            ["gw_port", "host"],
            registry=prom_registry
        ),
        "ds_client": prometheus_client.Counter(
            "tango_gateway_ds_client_connection",
            "Client connections to Device server",
            ["gw_port", "host"],
            registry=prom_registry
        ),
        "ds_request": prometheus_client.Counter(
            "tango_gateway_ds_request",
            "Client request to Device server",
            ["gw_port", "host"],
            registry=prom_registry,
        ),
        "zmq_event": prometheus_client.Counter(
            "tango_gateway_zmq_event",
            "ZMQ events",
            ["gw_port", "name", "db_host", "db_port"],
            registry=prom_registry
        ),
        "zmq_sub_change": prometheus_client.Counter(
            "tango_gateway_zmq_sub_change",
            "ZMQ_SUBSCRIPTION_CHANGE",
            ["gw_port", "host"],
            registry=prom_registry
        ),
    }
    prom_label_defaults = {"gw_port": 0}


def inc_counter(_counter_name, **labels):
    """Helper to increase a given Prometheus counter"""
    if prometheus_client:
        prom_counters[_counter_name].labels(**prom_label_defaults, **labels).inc()


async def write_counters(path, period=10):
    """Periodically write Prometheus metrics to disk"""
    while True:
        await asyncio.sleep(period)
        # Note that this is not done asynchronously. Hopefully this is a
        # pretty fast operation though.
        prometheus_client.write_to_textfile(path, prom_registry)


# Tokens

IMPORT_DEVICE = b'DbImportDevice'
GET_CSDB_SERVER = b'DbGetCSDbServerList'
ZMQ_SUBSCRIPTION_CHANGE = b'ZmqEventSubscriptionChange'


# Enumerations

class Patch(Enum):
    NONE = 0
    IOR = 1
    CSD = 2
    ZMQ = 3
    SUB = 4


class HandlerType(Enum):
    DB = 1
    DS = 2
    ZMQ = 3


# Function helpers

def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def make_translater(sub, pub):
    sub = ':'.join(map(str, sub)).encode()
    pub = ':'.join(map(str, pub)).encode()
    args = (sub, pub), (pub, sub)
    return lambda value, reverse=False: value.replace(*args[reverse])


# Coroutine helpers

async def get_connection(key, loop, only_check=False):
    host, port, _ = key
    # Try to connect
    try:
        reader, writer = await asyncio.open_connection(
            host, port)
    # Connection broken
    except (ConnectionRefusedError, OSError):
        logger.warn("Could not connect to {} port {}".format(host, port))
        if key != loop.db_key:
            await stop_forwarding(key, loop)
        return False
    # Connection OK
    if not only_check:
        return reader, writer
    writer.close()
    return True


async def get_host_name(stream, resolve=True):
    loop = stream._loop
    sock = stream._transport._sock
    if not resolve:
        return sock.getsockname()[0]
    name_info = await loop.getnameinfo(sock.getsockname())
    return name_info[0]


async def check_servers(loop, period=10.):
    while True:
        await asyncio.sleep(period)
        for key in list(loop.forward_dict):
            await get_connection(key, loop, only_check=True)


# Forwarding helpers

async def get_forwarding(host, port, handler_type,
                   bind_address='0.0.0.0', server_port=0, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    # Check cache
    key = host, port, bind_address
    if key in loop.forward_dict:
        return (await loop.forward_dict[key])
    # No connection check for DB
    if handler_type == HandlerType.DB:
        loop.db_key = key
    # Connection check
    elif not (await get_connection(key, loop, only_check=True)):
        return None, bind_address, loop.bound_port
    # Start forwarding
    loop.forward_dict[key] = asyncio.Future(loop=loop)
    value = await start_forwarding(
        host, port, handler_type, bind_address, server_port, loop)
    # Set cache
    loop.forward_dict[key].set_result(value)
    return value


async def start_forwarding(host, port, handler_type,
                     bind_address='0.0.0.0', server_port=0, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    # GIOP handler
    if handler_type != HandlerType.ZMQ:
        # Make handler
        key = host, port, bind_address
        handler_dict = {
            HandlerType.DB: handle_db_client,
            HandlerType.DS: handle_ds_client}
        handler = partial(handler_dict[handler_type], key=key)
        # Start server
        server = await asyncio.start_server(
            handler, bind_address, server_port,
            family=socket.AF_INET)
        bind_address, server_port = server.sockets[0].getsockname()
    # ZMQ handler
    else:
        # Make translater
        address = bind_address, loop.server_port
        translater = make_translater(address, loop.tango_host)
        # Start server
        coro = zmqforward.pubsub_forwarding(
            host, port, translater, bind_address, server_port, loop=loop)
        server, bind_address, server_port = await coro
    # Print and return
    msg = "Forwarding {} traffic on {} port {} to {} port {}"
    msg = msg.format(handler_type.name, bind_address, server_port, host, port)
    inc_counter("forwarding",
                src_host=bind_address, src_port=server_port,
                dst_host=host, dst_port=port)
    logger.info(msg)
    return server, bind_address, server_port


async def stop_forwarding(key, loop):
    # Get server
    if key not in loop.forward_dict or \
       not loop.forward_dict[key].done() or \
       loop.forward_dict[key].exception():
        return
    server, bind_address, server_port = loop.forward_dict.pop(key).result()
    # Close server
    server.close()
    await server.wait_closed()
    # Print
    host, port, _ = key
    msg = "Stopped forwarding traffic on {} port {} to {} port {}"
    logger.info(msg.format(bind_address, server_port, host, port))


# Frame helper

async def forward_giop_frame(reader, writer, bind_address, patch=Patch.NONE):
    last = False
    while not last:
        last, fragment = await read_giop_fragment(
            reader, bind_address, patch)
        if fragment:
            writer.write(fragment)
    return fragment


async def read_giop_fragment(reader, bind_address, patch=Patch.NONE):
    # Read header
    loop = reader._loop
    try:
        raw_header = await reader.readexactly(12)
    except asyncio.IncompleteReadError:
        return True, b''
    header = giop.unpack_giop_header(raw_header)
    last = giop.is_last_fragment(header)
    # Read data
    raw_data = await reader.readexactly(header.size)
    raw_frame = raw_header + raw_data
    if header.message_type != giop.MessageType.Reply or patch == Patch.NONE:
        return last, raw_frame
    # Unpack reply
    raw_reply_header, raw_body = raw_data[:12], raw_data[12:]
    reply_header = giop.unpack_reply_header(raw_reply_header)
    if reply_header.reply_status != giop.ReplyStatus.NoException:
        return last, raw_frame
    assert giop.is_little_endian(header)
    # Patch body
    if patch == Patch.IOR:
        new_body = await check_ior(raw_body, bind_address, loop)
    elif patch == Patch.ZMQ:
        new_body = await check_zmq(raw_body, bind_address, loop)
    elif patch == Patch.CSD:
        new_body = await check_csd(raw_body, bind_address, loop)
    # Ignore
    if not new_body:
        return last, raw_frame
    # Repack frame
    raw_data = raw_reply_header + new_body
    return last, giop.pack_giop(header, raw_data)


# Inspect DB traffic

async def handle_db_client(reader, writer, key):
    with closing(writer):
        loop = reader._loop
        bind_address = await get_host_name(writer)
        inc_counter("db_client", host=bind_address)
        # Connect to client
        connection = await get_connection(key, loop)
        if not connection:
            return
        db_reader, db_writer = connection
        # Loop over reply/requests
        with closing(db_writer):
            while not reader.at_eof() and not db_reader.at_eof():
                # Read request
                request = await forward_giop_frame(
                    reader, db_writer, bind_address)
                if not request:
                    break
                # Choose patch
                if IMPORT_DEVICE in request:
                    patch = Patch.IOR
                elif GET_CSDB_SERVER in request:
                    patch = Patch.CSD
                else:
                    patch = Patch.NONE
                # Read reply_header
                reply = await forward_giop_frame(
                    db_reader, writer, bind_address, patch=patch)


async def check_ior(raw_body, bind_address, loop):
    # Find IOR, host and port
    ior = giop.find_ior(raw_body)
    if not ior:
        return False
    ior, start, stop = ior
    host = giop.from_byte_string(ior.host)
    # Start port forwarding
    server, _, server_port = await get_forwarding(
        host, ior.port, HandlerType.DS, bind_address, loop=loop)
    # Patch IOR
    ior = ior._replace(host=giop.to_byte_string(bind_address),
                       port=server_port)
    # Log tango device name
    try:
        device_name = giop.find_device_name(raw_body, start-4)
        logger.info("Providing access to device {}".format(device_name))
        inc_counter("client_connection", device=device_name, src_host=bind_address, src_port=server_port, dst_host=host, dst_port=ior.port)
    except ValueError:
        msg = "Could not get device name in {} reply"
        logger.warn(msg.format(IMPORT_DEVICE))
    # Repack body
    return giop.repack_ior(raw_body, ior, start, stop)


async def check_csd(raw_body, bind_address, loop):
    csd = giop.find_csd(raw_body)
    if not csd:
        return False
    csd, start = csd
    new_csd = ':'.join((bind_address, str(loop.server_port)))
    new_csd = giop.to_byte_string(new_csd)
    return giop.repack_csd(raw_body, new_csd, start)


# Inspect DS traffic

async def handle_ds_client(reader, writer, key):
    with closing(writer):
        loop = reader._loop
        bind_address = await get_host_name(writer)
        inc_counter("ds_client", host=bind_address)
        # Connect to client
        connection = await get_connection(key, loop)
        if not connection:
            return
        ds_reader, ds_writer = connection
        # Loop over reply/requests
        with closing(ds_writer):
            while not reader.at_eof() and not ds_reader.at_eof():
                # Read request
                request = await forward_giop_frame(
                    reader, ds_writer, bind_address)
                if not request:
                    break
                # Choose patch
                if ZMQ_SUBSCRIPTION_CHANGE in request:
                    inc_counter("zmq_sub_change", host=bind_address)
                    patch = Patch.ZMQ
                else:
                    inc_counter("ds_request", host=bind_address)
                    patch = Patch.NONE
                # Read reply_header
                await forward_giop_frame(
                    ds_reader, writer, bind_address, patch=patch)


async def check_zmq(raw_body, bind_address, loop):
    # Find zmq token
    result = giop.find_zmq_endpoints(raw_body)
    if not result:
        return False
    # Filter endpoints
    endpoints, start = result
    nb = len(endpoints)
    if nb > 2:
        logger.info('Discarding {}/{} endpoints'.format(nb-2, nb))
        endpoints = endpoints[:2]
    # Exctract endpoints
    new_endpoints = []
    for endpoint in endpoints:
        host, port = giop.decode_zmq_endpoint(endpoint)
        # Start port forwarding
        _, zmq_bind_address, server_port = await get_forwarding(
            host, port, HandlerType.ZMQ, bind_address, loop=loop)
        # Make new endpoints
        new_endpoint = giop.encode_zmq_endpoint(zmq_bind_address, server_port)
        new_endpoints.append(new_endpoint)
    # Extract event sources
    # For tango >= 9.3.0 (ZMQ Topics are now returned by the server)
    (tango_names, _) = giop.find_tango_names(raw_body)
    for tango_name in tango_names:
        host, port, name = giop.decode_tango_name(tango_name)
        inc_counter("zmq_event", db_host=host, db_port=port, name=name)
        if None not in [host, port, name]:
            # Make new names
            new_tango_name = giop.encode_tango_name(
                bind_address, loop.server_port, name)
            new_endpoints.append(new_tango_name)
    # Repack body
    return giop.repack_zmq_endpoints(raw_body, new_endpoints, start)


# Run server

def run_gateway_server(bind_address, server_port, tango_host, debug=True, promfile=None):
    """Run a Tango gateway server."""
    # Configure logger
    if debug:
        logger.setLevel(logging.DEBUG)

    # Initialize loop
    loop = asyncio.get_event_loop()
    loop.bind_address = bind_address
    loop.server_port = server_port
    loop.tango_host = tango_host
    loop.forward_dict = {}
    loop.bound_socket = socket.socket()
    loop.bound_socket.bind((bind_address, 0))
    loop.bound_port = loop.bound_socket.getsockname()[1]

    # Promerheus monitoring
    if prometheus_client and promfile:
        prom_label_defaults.update({"gw_port": server_port})
        loop.create_task(write_counters(promfile))

    # Create server
    host, port = tango_host
    loop.run_until_complete(get_forwarding(
        host, port, HandlerType.DB, bind_address, server_port, loop=loop))
    # Serve requests until Ctrl+C is pressed
    try:
        check_task = loop.create_task(check_servers(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        check_task.cancel()
    # Close all the servers
    servers = [fut.result()[0]
               for fut in loop.forward_dict.values()
               if fut.done() and not fut.exception()]
    for server in servers:
        server.close()
    # Wait for the servers to close
    wait_servers_tasks = [loop.create_task(server.wait_closed()) for server in servers]
    wait_servers = asyncio.wait(wait_servers_tasks)
    loop.run_until_complete(wait_servers)
    # Cancel all the tasks
    tasks = asyncio.all_tasks(loop)
    for task in tasks:
        task.cancel()
    # Wait for all the tasks to finish
    if tasks:
        loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
