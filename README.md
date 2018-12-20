"# snes_mini_xml_to_tabular" 

## Introductions
As a result of understanding how games are loaded to the Hakchi2 via a USB drive,
the folder structure continued to become increasing more labyrinthine in nature.

This tool translates the SNES Minis XML file structure format to the command line and tab delimited txt file which will aim to alleviate that issue. 

## Getting Started
1. Locate the "folders_snes_usa.xml" file in: hakchi2-ce\hakchi2-ce-x.y.z-debug\config
2. Copy/Cut the file into this working directory.
3. Execute the following command ``python xml_to_tabular.xml large_sample_folders_snes_usa.xml`` 
4. The command line output should be sorted by system.
Under each system should be the name of the game along with the folder where
it can be located. It should also generate a text file with the name 'mini_games_tab_delimited.txt' in a tabular format
5. The column headers for the text file should be 'Console Name', 'Title' and 'File/Folder Name'

## Usage Example
``python xml_to_tabular.xml large_sample_folders_snes_usa.xml``

## Contributing
1. Fork the project
2. Create a new feature brach on the fork project
3. Commit changes
4. Push the changes to the branch.
5. Create a new Pull Request back to the main project

## Contributing

Many thanks to the SNES Hakchi modding community.
None of the functionality here would be possible without their base tools to work with