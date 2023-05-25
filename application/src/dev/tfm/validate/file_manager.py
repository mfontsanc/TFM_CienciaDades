import os


class FileManager:
    @staticmethod
    def validate_folder_path(path):
        """
            Method to validate that the path exists, it is a folder.

            Parameters:
                path(str): String with a path to validate.

            Returns:
                Bool: whether folder_path is a folder and exists or not.
        """
        if os.path.exists(path) and os.path.isdir(path):
            return True
        return False

    @staticmethod
    def create_folder(path: str):
        """
            Method to validate whether the folder exists, if not it creates it.

            Parameters:
                path(str): String with the path to create.

            Returns:
                None
        """
        if not FileManager.validate_folder_path(path):
            os.mkdir(path)

    @staticmethod
    def remove_file(filename: str):
        """
            Remove file from a specific path.

            Parameters:
                filename(str): String with the path of the file.

            Returns:
                None
        """
        if os.path.exists(filename):
            os.remove(filename)
