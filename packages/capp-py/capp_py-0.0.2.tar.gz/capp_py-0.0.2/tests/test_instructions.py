import pytest
from capp.instructions import (
    Code,
    ErrorCode,
    Request,
    RequestAppendStream,
    RequestCloseStream,
    RequestConnect,
    RequestDisconnect,
    RequestFlushStream,
    RequestHeatbeat,
    RequestOpenStream,
    RequestReconnect,
    Response,
    ResponseAppendStream,
    ResponseCloseStream,
    ResponseConnect,
    ResponseDisconnect,
    ResponseError,
    ResponseFlushStream,
    ResponseHeartbeat,
    ResponseOpenStream,
    ResponseReconnect,
    Status,
)


@pytest.mark.parametrize(
    "code, payload",
    [
        (Code.CONNECT, RequestConnect()),
        (Code.DISCONNECT, RequestDisconnect(client_id=123)),
        (Code.OPEN_STREAM, RequestOpenStream(client_id=123, filepath="/tmp/abc.txt")),
        (
            Code.APPEND_STREAM,
            RequestAppendStream(client_id=123, stream_id=2, data=b"Hello"),
        ),
        (Code.FLUSH_STREAM, RequestFlushStream(client_id=123, stream_id=3)),
        (Code.CLOSE_STREAM, RequestCloseStream(client_id=123, stream_id=4)),
        (Code.HEARTBEAT, RequestHeatbeat(client_id=123, acked_seq_num=456789)),
        (Code.RECONNECT, RequestReconnect(client_id=123)),
    ],
)
def test_request_encode_decode(code, payload):
    req = Request(seq_num=1, code=code, payload=payload)
    wire = req.encode()
    decoded = Request.decode(wire)
    assert decoded == req


@pytest.mark.parametrize(
    "status, code, payload",
    [
        (Status.OK, Code.CONNECT, ResponseConnect(client_id=123)),
        (Status.OK, Code.DISCONNECT, ResponseDisconnect()),
        (Status.OK, Code.OPEN_STREAM, ResponseOpenStream(stream_id=1)),
        (Status.OK, Code.APPEND_STREAM, ResponseAppendStream()),
        (Status.OK, Code.FLUSH_STREAM, ResponseFlushStream()),
        (Status.OK, Code.CLOSE_STREAM, ResponseCloseStream()),
        (Status.OK, Code.HEARTBEAT, ResponseHeartbeat()),
        (Status.OK, Code.RECONNECT, ResponseReconnect()),
        (
            Status.ERROR,
            None,
            ResponseError(code=ErrorCode.INVALID_REQUEST, err="Invalid request"),
        ),
    ],
)
def test_response_encode_decode(status, code, payload):
    resp = Response(seq_num=123, status=status, code=code, payload=payload)
    wire = resp.encode()
    decoded = Response.decode(wire)
    assert decoded == resp
