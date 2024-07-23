from ewoksnotify.tasks.get_from_data import GetFromDataTask


# Adapt this test for dictionary and not only list type of data
# Test with a list
def test_list():
    list_task = GetFromDataTask(
        inputs={
            "data": [1, 2, 3, 4, 5],
            "index": 0,
        },
    )
    list_task.run()
    assert list_task.outputs.element == 1, "Failed list test!"


# Test with a dict
def test_dict():
    dict_task = GetFromDataTask(
        inputs={
            "data": {"a": 100, "b": 200, "c": 300},
            "index": "a",
        },
    )
    dict_task.run()
    assert dict_task.outputs.element == 100, "Failed dict test!"
