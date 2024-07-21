import capp
from capp import wireformat as wf


def test_string():
    buf = bytearray()
    input_str = "hello 你好 🤔"
    wf.encode_string(input_str, buf)
    decoded_str, _ = wf.decode_string(buf)
    assert decoded_str == input_str


def test_numerical_id():
    buf = bytearray()
    input_id = capp.NumericalID(123456789)
    assert input_id < 2**31 - 1
    wf.encode_numerical_id(input_id, buf)
    decoded_id, _ = wf.decode_numerical_id(buf)
    assert decoded_id == input_id


def test_seq_num():
    buf = bytearray()
    input_seq_num = capp.SeqNum(2**40 + 123)
    assert input_seq_num < 2**63 - 1
    wf.encode_seq_num(input_seq_num, buf)
    decoded_seq_num, _ = wf.decode_seq_num(buf)
    assert decoded_seq_num == input_seq_num
