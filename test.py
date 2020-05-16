from version import list_versions, sort_versions, get_meta_file, save_file


def test_get_meta_file(_s3):
    assert get_meta_file("proxyroot/test.txt") == []


def test_list_versions_happy_path(_s3, mocker):
    _s3["client"].put_object(
        Bucket="bucket.proxyroot.com", Key="proxyroot/test.txt", Body="scan stl file"
    )
    expected = [{"created": mocker.ANY, "id": mocker.ANY}]

    assert list_versions("proxyroot/test.txt") == expected

    _s3["client"].put_object(
        Bucket="bucket.proxyroot.com", Key="proxyroot/test.txt", Body="scan stl file"
    )
    expected = [
        {"created": mocker.ANY, "id": mocker.ANY},
        {"created": mocker.ANY, "id": mocker.ANY},
    ]
    assert list_versions("proxyroot/test.txt") == expected


def test_sort_versions():
    versions = [
        {"id": "kjksdf", "created": "April 23, 2019"},
        {"id": "asdf", "created": "April 21, 2019"},
    ]
    expected = [
        {"id": "asdf", "created": "April 21, 2019"},
        {"id": "kjksdf", "created": "April 23, 2019"},
    ]
    assert sort_versions(versions) == expected


def test_save_file(_s3, mocker):
    versions = save_file("proxyroot", "test2.txt", "Hello World", "first")

    assert versions == [{"created": mocker.ANY, "name": "first"}]

    versions = save_file("proxyroot", "test2.txt", "Hello World\nHello World", "second")

    assert versions == [
        {"created": mocker.ANY, "name": "first"},
        {"created": mocker.ANY, "name": "second"},
    ]
