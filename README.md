# Naming Convention App for Shotgun Toolkit
![foto_obs_logo.png](./screenshots/foto_obs_logo.png)
#### The Griffith Observatory and Friends Of The Observatory Satellite Studio is proud to share the Toolkit Naming Convention app that was developed for _Signs of Life_. This new show premieres in May, 2020, in the Samuel Oschin Planetarium at Griffith Observatory, Los Angeles.
#### Astronomically yours!
http://www.griffithobservatory.org/
<br>http://www.friendsoftheobservatory.com
***
![tk-multi-namingconvention.png](./screenshots/foto-multi-namingconvention.png)

##### The Naming Convention Toolkit App provides a convenient and easy way for artists to work with the studio defined Toolkit naming conventions and directory structures.
##### This is particularly useful for DCC applications that don't have Toolkit integration but need to have files put into the proper directory and follow a certain naming convention.
##### The "Copy File to File Path" feature allows the artist to copy a single file to the "File Path" defined above. Image sequences are not currently supported.
##### It can also be useful as a stop gap tool while the pipeline is being built out but production is moving forward.

##### Feel free to reach out to me with any questions or use case issues.

##### Cheers,
##### Scott Ballard
* scott@scottballard.net
* https://www.linkedin.com/in/scottballard/
***
## Using the Naming Convention App

![tk-multi-namingconvention instructions.png](./screenshots/foto-multi-namingconvention-instructions.png)

#### Step 1 - Select Shotgun Context (Task)
Using the Toolkit context widget, select the Shotgun Task you are working with that you want to create the associated file or directory
#### Step 2 - Select Application
Select the DCC application you are working with. When you do, Toolkit will register the selected context and application.
![foto-multi-namingconvention registering.png](./screenshots/foto-multi-namingconvention-registering.png)
#### Step 3 - Select Toolkit Template
Select the associated Toolkit template. The description (below) might be helpful to know which template to use
#### Step 4 - Toolkit Template Description
This field may provide a further description of the Toolkit template selected above and how to use it
#### Step 5 - Toolkit Template Tokens
* Some Toolkit templates require extra token data that can be changed by the artist. Default values are usually provided.
The description above may provide additional information about the tokens
* The artist may need to provide additional values for the extra tokens
#### Step 6 - File Name
* The basename of the file derived from the Toolkit template
#### Step 7 - Directory Path
* The directory derived from the selected Toolkit template
#### Step 8 - File Path
* The full file path derived from the selected Toolkit template
#### Step 9 - Copy File to File Path
* Use this to copy a file into the same file path that is defined in the "File Path" above.
* Drag & Drop a file onto the widget or use the file browser button to the right.
#### Step 10 - Copy File Name
* Button will copy the "File Name"
#### Step 11 - File Browse / Copy Directory Path
* "Browse" button (first) will open a File Explorer or Finder window to the "Directory Path"
* "Copy" button (second) will copy the "Directory Path"
#### Step 12 - Copy File to File Path
* "Plus" button (first) will create the "File Path" on disk 
* "Browse" button (second) will open a File Explorer or Finder window to the "File Path"
* "Copy" button (second) will copy the "File Path"
#### Step 13 - Copy File to File Path
* "Browse" button (first) will open a File selection dialog to select the file you want to copy

***
## Installation
**Important:** The Toolkit template path keys are a bit inconsistent. To use this tool your template keys must be in the 
    format "< entity >_< engine >".
    
    examples:
        shot_maya_work
        shot_maya_playblast
        shot_maya_render_folder

#### Setup
If you want to get up and running quickly, follow this simple step:
* tank install_app Project tk-desktop https://github.com/scottb08/foto-multi-namingconvention.git

#### Known Issues
* Toolkit's context selector widget has a known issue that if the context isn't registered with TK
  the "name" of the entity isn't returned internally and the widget fails to populate any values.

## Optional Configuration Fields

#### template_definitions
    type: dict
    allows_empty: True
    description: Toolkit itself does not provide a method of defining descriptions for template definitions, that would be useful for artists. 
    The Naming Convention tool allows regular expressions to be defined and associated descriptions, 
    which can be used to define descriptions for those template entries. 
    
    The key is a regex that matches a template key, the value is the description you want to provide the artist.
    
    examples:
        work$: The artist "working" file where you should write your file to
        work area$: This is the artist "working" directory where you should store your working files
        pub$: The publish file for the selected application
        pub area$: The publish directory for the selected application
        render$: The render output directory for the selected application
        camera pub$: The camera publish path for the selected application
    
#### restrict_entity_types_by_link
    type: dict
    allows_empty: True
    description: Specify what entries should show up in the list of links when using the auto completer.
      dictionary should contain two key value pairs; entity name and entity field name.
          entity: <PublishedFile>
          field: <entity>

      For the simple case where you just want to show a given set of
      entity types, use :meth:`restrict_entity_types`. This method is
      a more complex restriction suitable for workflows around publishing
      and review.

      This method will look at the given link field (e.g. ``PublishedFile.entity``)
      and inspect the shotgun schema to see which entity types are valid connections
      to this field (e.g. in this example which entity types can you can associate
      a publish with) and those types will appear in the list of items shown by the
      auto completer.

      This is useful when you want to use the context widget in conjunction with
      workflows related to for example publishes, versions or notes and you want to
      restrict the entities displayed by the auto completer to the ones that have been
      configured in the shotgun site schema to be able to associate with the given type.
    default_value: {}
    
    examples:
        entity: PublishedFile
        field: entity

#### restrict_entity_types
    type: list
    description: Restrict which entity types should show up in the list of matches. List of entity names
    values:
      type: str
    allows_empty: True
    default_value: []
    
    example:
        - Asset
        - MocapTake
        - Shot

#### custom_entity_name_remap
    type: dict
    allows_empty: True
    description: Remap the SG internal entity name to match the entity token in the TK template definition.
        Value gets converted to lower case internally to match TK template definition.
    default_value: {}
    
    examples:
        MocapTake: Take (ie: TK template definition take_maya_work)
        Shot: MyShot    (ie: TK template definition myshot_maya_work)

#### tk-engines
    type: dict
    allows_empty: False
    description: A dict of tk-engines (as defined in the TK schema, can be unsupported engines)
    
    examples:
        AfterEffects: tk-aftereffects
        Data: data     <-- non-tk-engine, matches template definition ex: shot_data_asset_element (<entity>_<engine>) 
        Mari: tk-mari
        Maya: tk-maya
        Motion Builder: tk-motionbuilder
        Photoshop: tk-ps
        Nuke: tk-nuke
