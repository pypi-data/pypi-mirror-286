from ewokscore.task import Task


# Adapt this class for dictionary and not only list type of data
class GetFromDataTask(
    Task,
    input_names=("data", "index"),  # type: ignore
    output_names=("element",),  # type: ignore
):
    """
    Return an element from a data that can be a list or a dict.
    """

    def run(self):
        input_data = self.inputs.data
        input_index = self.inputs.index

        # Check data type
        if isinstance(input_data, list):
            # Extract element from a list
            # Check if the key is out of range
            if input_index < len(input_data):
                self.outputs.element = input_data[input_index]
            else:
                raise IndexError("Error: The index is out of range!")

        elif isinstance(input_data, dict):
            # Extract element from a dict
            # Check if the key is in the dictonary
            if input_index in input_data:
                self.outputs.element = input_data[input_index]
            else:
                raise KeyError("Error: Key not found in the dictonary")

        else:
            raise TypeError("Error: The data should be a list or a dict!")
