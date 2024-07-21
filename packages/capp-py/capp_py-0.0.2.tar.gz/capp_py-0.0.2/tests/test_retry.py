from capp.retry import NoRetry


def test_no_retry():
    no_retry = NoRetry()
    retrier = no_retry.create_retrier()
    count = 0
    for _ in retrier:
        count += 1
    assert count == 1
