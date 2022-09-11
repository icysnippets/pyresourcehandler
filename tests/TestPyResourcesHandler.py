import os
import tempfile
from pathlib import Path
import pytest

from src.pyResourceHandler import extractFile, extractDir

#Path to the embedded file
_resourceFile = "file_example.txt"

#Path to the invalid ".py" file
_resourceInvalidPyFile = "invalid_python_example.py"

#Path to the embedded directory
_resourceDir = "dir_example"

class TestPyResourcesHandler:
    def testGetResourcesRootFailure(self):

        """
        Attempts to extract a file from a module with a data folder.
        Should fail since module does not use a predefined data-folder name.
        Expects failure.
        """

        try:

            with tempfile.TemporaryFile() as tmpFile:

                #Attempt to extract a file
                extractFile(
                    "tests.Example_Module_Bad", #Intentionally incorrect
                    _resourceFile,
                    tmpFile
                )

            # Create the error message
            errorMsg = f"'{extractFile.__name__}' should not have found the module"
            pytest.fail(errorMsg)

        except FileNotFoundError:

            #Do nothing since this is expected behaviour
            pass

    def testExtractFile(self):

        """
        Makes sure that regular files are extracted correctly.
        """

        #Iterate twice to test the 'overwrite' argument
        for i in range(2):

            with tempfile.TemporaryDirectory() as tmpDir:

                #Output path for the resource file
                outputPath = Path(tmpDir, _resourceFile)

                #Make sure the directory has 0 files
                assert 0 == len(os.listdir(tmpDir))

                #Create the file for the second iteration
                if i == 1: outputPath.write_text("")

                extractFile(
                    "tests.Example_Module",
                    _resourceFile,
                    outputPath,
                    overwrite=i == 1  # Overwrite the file created in the 2nd iteration
                )

                #Make sure the directory has exactly 1 file
                assert 1 == len(os.listdir(tmpDir))

                #Read the contents of the extracted resource file
                contents = outputPath.read_text(encoding="utf-8")

                #Make sure the file contains the correct content
                assert contents == "123"

    def testExtractFileFail(self) -> None:

        """
        Attempts to extract a directory using the method for files.
        Expects failure.
        """

        try:

            with tempfile.TemporaryFile() as tmpFile:

                #Attempt to extract a directory using the method for files
                extractFile(
                    "tests.Example_Module",
                    _resourceDir, #Intentionally incorrect
                    tmpFile
                )

            # Create the error message
            errorMsg = f"'{extractFile.__name__}' should fail to extract/find directories"
            pytest.fail(errorMsg)

        except FileNotFoundError:

            #Do nothing since this is expected behaviour
            pass

    def testExtractFileFail2(self) -> None:

        """
        Attempts to extract a file to an existing file without specifying overwrite.
        Expects failure.
        """

        try:

            with tempfile.TemporaryDirectory() as tmpDir:

                # Output path for the resource file
                outputPath = Path(tmpDir, _resourceFile)

                #Ensure the file exists
                outputPath.write_text("")

                #Attempt to extract a file
                extractFile(
                    "tests.Example_Module",
                    _resourceFile,
                    outputPath,
                    overwrite=False #Intentionally incorrect
                )

            # Create the error message
            errorMsg = f"'{extractFile.__name__}' should fail to overwrite files without 'overwrite' option"
            pytest.fail(errorMsg)

        except FileExistsError:

            #Do nothing since this is expected behaviour
            pass

    def testExtractInvalidPyFile(self) -> None:

        """
        Makes sure that invalid python files packaged as resources are extracted correctly.
        """
        with tempfile.TemporaryDirectory() as tmpDir:

            #Output path for the resource file
            outputPath = Path(tmpDir, _resourceInvalidPyFile)

            #Make sure the directory has 0 files
            assert 0 == len(os.listdir(tmpDir))

            extractFile(
                "tests.Example_Module",
                _resourceInvalidPyFile,
                outputPath
            )

            #Make sure the directory has exactly 1 file
            assert 1 == len(os.listdir(tmpDir))

            #Read the contents of the extracted resource file
            contents = outputPath.read_text(encoding="utf-8")

            #Make sure the file contains the correct content
            assert contents == "print(hello world)"

    def testExtractDir(self) -> None:

        """
        Makes sure that invalid python files packaged as resources are extracted correctly.
        """

        #Iterate twice to test the 'overwrite' argument
        for i in range(2):

            with tempfile.TemporaryDirectory() as tmpDir:

                #Create the directory for the second iteration
                if i == 1: Path(tmpDir).mkdir(exist_ok=True, parents=True)

                #Output path for the resource file
                outputPath = Path(tmpDir, _resourceDir)

                #Make sure the directory has 0 files
                assert 0 == len(os.listdir(tmpDir))
                assert False == outputPath.is_dir()

                extractDir(
                    "tests.Example_Module",
                    _resourceDir,
                    outputPath,
                    overwrite = i == 1 #Overwrite the directory created in the 2nd iteration
                )

                #Make sure the directory has exactly 1 directory
                assert 1 == len(os.listdir(tmpDir))
                assert True == outputPath.is_dir()

                #Create the path to the expected files
                helloWorld1 = outputPath.joinpath("hello world 1.txt")
                helloWorld2 = outputPath.joinpath("nested_dir", "hello world 2.txt")

                #Make sure the expected files hold the correct content
                assert "hello world 1" == helloWorld1.read_text()
                assert "hello world 2" == helloWorld2.read_text()

    def testExtractDirFail(self) -> None:
        """
        Attempts to extract a file using the method for directories.
        Expects failure.
        """

        try:

            with tempfile.TemporaryDirectory() as tmpDir:

                #Attempt to extract a file using the method for directories
                extractDir(
                    "tests.Example_Module",
                    _resourceFile, #Intentionally incorrect
                    tmpDir
                )

            # Create the error message
            errorMsg = f"'{extractDir.__name__}' should fail to extract/find files"
            pytest.fail(errorMsg)

        except FileNotFoundError:

            #Do nothing since this is expected behaviour
            pass

    def testExtractDirFail2(self) -> None:

        """
        Attempts to extract a directory to an existing file without specifying overwrite.
        Expects failure.
        """
        try:

            with tempfile.TemporaryDirectory() as tmpDir:

                # Output path for the resource directory
                outputPath = Path(tmpDir, _resourceDir)

                #Ensure the directory exists
                outputPath.mkdir(parents=True)

                #Attempt to extract a directory
                extractDir(
                    "tests.Example_Module",
                    _resourceDir,
                    outputPath,
                    overwrite=False #Intentionally incorrect
                )

            # Create the error message
            errorMsg = f"'{extractFile.__name__}' should fail to overwrite directories without 'overwrite' option"
            pytest.fail(errorMsg)

        except FileExistsError:

            #Do nothing since this is expected behaviour
            pass

