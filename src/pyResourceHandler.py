import importlib.resources
import shutil
from importlib.abc import Traversable
from pathlib import Path

def _loadModule(modulePath: str) -> Traversable:

    """
    Gets a Traversable resource from the given module path.

    :param modulePath: Path to the module.
    :return: Returns a Traversable object.
    """

    return importlib.resources.files(modulePath)

def _getResourcesRoot(modulePath: str) -> Traversable:

    """
    Gets the resources root of a given module.
    Module should contain a directory in its root with one of the following names:
    -resources
    -data
    -assets

    :param modulePath: Path to the module.
    :return: Returns Traversable object to the resource root.
    """
    #Get the module
    module = _loadModule(modulePath)

    #List of possible names for the resource root
    resourceRootNames = ["resources", "data", "assets"]

    #Iterate through the list of possible resource root names
    for resourceRootName in resourceRootNames:

        # Attempt to find the resource root
        resourceRoot = module \
            .joinpath(resourceRootName)

        #If the resource root was successfully found
        if resourceRoot.is_dir():

            #Return the resources root
            return resourceRoot

    #Create the error message
    errorMsg = f"No resources directory found in module {modulePath}\n"
    errorMsg += "Resource directory should be named one of the following:\n"
    for resourceRootName in resourceRootNames: errorMsg += f"-{resourceRootName}\n"
    raise FileNotFoundError(errorMsg)

def extractFile(
    modulePath: str,
    resourceFile: str,
    outputPath: Path,
    overwrite: bool = False
):

    """
    Extracts a resource file embedded within the application.

    :param modulePath: Path to import module
    :param resourceFile: Path expression to the resource file.
    :param outputPath: Path to the output file.
    :param overwrite: Whether the output file should be overwritten if it already exists.
    """

    #Load the resources root
    module = _getResourcesRoot(modulePath)

    #Get the resource at the given path
    resource = module \
        .joinpath(resourceFile)

    #Determine whether a file is found at the given path
    fileFound = resource.is_file()

    #If no file was found matching the given expression
    if not fileFound:

        #Create an error message
        errorMsg = f"No file found matching expression '{resourceFile}'"

        #Throw an error message here
        raise FileNotFoundError(errorMsg)

    #Ensure the output path's parent directory exists
    outputPath.parent.mkdir(
        exist_ok=True,
        parents=True
    )

    #If the output file should not be overwritten
    if overwrite == False and outputPath.exists():

        #Create the error message
        errorMsg = f"'{outputPath}' already exists\n"
        errorMsg += "Cannot overwrite existing file"

        #Throw the error
        raise FileExistsError(errorMsg)

    #Write the contents to the file
    with open(outputPath, "wb") as outputFile:

        #Extract the content of the embedded resource file
        outputFile.write(resource.read_bytes())

def _iterateDir(resource: Traversable) -> list[Traversable]:

    """
    Gets a recursive list of all files(including directories).

    :param resource: Expected to be a directory.
    :return: Returns a list of traversable objects.
    """

    #Create a list to store the resources including the current resource
    resources = []

    #Iterate through the resources in this directory
    for f in resource.iterdir():

        #If the current file is a directory
        if f.is_dir():

            #Add this directory to the list of resources
            resources.append(f)

            #Add the list of resources within this subdirectory
            resources.extend(_iterateDir(f))

        #If this is a file
        else:

            resources.append(f)

    #Return the list of resources
    return resources

def extractDir(
        modulePath: str,
        resourceFile: str,
        outputDir: Path,
        overwrite: bool = False
):
    """
    :param modulePath: Path to import module
    :param resourceFile: Path expression to the resource directory.
    :param outputDir: Path to the output directory.
    :param overwrite: Whether the output directory should be overwritten if it already exists.
    """

    # Load the resources root
    module = _getResourcesRoot(modulePath)

    #Get the resource at the given path
    resource = module \
        .joinpath(resourceFile)

    #Determine whether a directory is found at the given path
    directoryFound = resource.is_dir()

    #If no directory was found matching the given expression
    if not directoryFound:

        #Create an error message
        errorMsg = f"No directory found matching expression '{resourceFile}'"

        #Throw an error message here
        raise FileNotFoundError(errorMsg)

    #If the output directory should not be overwritten
    if overwrite == False and outputDir.exists():

        #Create the error message
        errorMsg = f"'{outputDir}' already exists\n"
        errorMsg += "Cannot overwrite existing directory"

        #Throw the error
        raise FileExistsError(errorMsg)

    #Delete the existing directory(if one exists)
    if outputDir.exists(): shutil.rmtree(outputDir)

    #Ensure the output directory exists
    outputDir.mkdir(parents=True)

    # Get a recursive list of files in the directory
    filesRecursiveList = _iterateDir(resource)

    # Iterate through the list of files
    for f in filesRecursiveList:

        # Get the relative path for this resource
        relativePath = str(f).replace(str(resource), "")

        # Create the output path for this resource
        outputPath = Path(
            f"{outputDir}/{relativePath}"
        )

        # If the resource is a directory
        if f.is_dir():

            # Ensure the directory is created
            outputPath.mkdir(exist_ok=True, parents=True)

        # Else if the resource is a file
        else:

            # Write the contents to the file
            with open(outputPath, "wb") as outputFile:

                # Extract the content of the embedded resource file
                outputFile.write(f.read_bytes())