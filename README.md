HyLECA: *Hy*brid *L*ong-term *E*ngaging *C*ontrolled Conversational *A*gents Development Framework
==================================================================================================

This repository contains the conversational agent (a.k.a. chatbot) dialogue management system developed to conduct the chatbot experiments described in the context of [Look Who's Talking](https://look.uvt.nl) project. For more information on Look Who's Talking project, please visit [https://look.uvt.nl](https://look.uvt.nl).

Installation & Setup
--------------------
The system is developed by using **Python 3.8.10**.
It is tested in _Linux Mint 20.3_ and _Ubuntu SMP 18.04_ operating systems. 
The example commands given in this tutorial below are mainly for usage in Linux. 
They may be adapted to be used in other operating systems as well.

1. Create a Python virtual environment. In te example below, the Linux command creates a Python 3 environment named `.env` as a hidden folder.

    ```bash
    # Run the following command inside the "hyleca" folder.
    python3 -m venv .env
    ```

2. Install the contents of the `hyleca/requirements.txt` within the virtual environment.

    ```bash
    # Activate the virtual environment
    source activate .env
    # Install the packages given in "requirements.txt"
    pip install -r requirements.txt
    ```
3. The system uses spaCy Python library and its models. Install at least the English model below, which is required. 

    ```bash
    # Run the following command inside the virtual environment
    python -m spacy download en_core_web_lg
    ```

4. Modify the `hyleca/config-template.yml` to fill in your own relevant data. Please see the file itself for further instructions on each required key. If you decide to rename the config file (e.g. as `config.yml`), do not forget to change the file name in the following steps as well.

5. Export the absolute path of your config file to an environment variable called `CONFIG_PATH`. 

    ```bash
    # Following is an example bash command to export the environmental variable. 
    # Some Python IDEs may require you to do this within their own user interface.
    export CONFIG_PATH="< insert your absolute directory path to the hyleca folder >/hyleca/config-template.yml"
    ```
6. Now you should be able to use `hyleca/tests/test_talk.py` to test your bots via the command line system or the interpreter of the IDE. **Do not forget** to set the `BOT_TOKEN` global variable inside the file to the unique token of your bot before running the script. See the file for further instructions.

Folder Structure
----------------
The list of folders and important scripts and their brief descriptions:

- `bots`: Contains the folders that are relevant to the dialogue designs for each bot developed for this project. Each folder should belong to an independent bot.
  - `bots/example-bot`: The folder contains a mock-up bot that displays the basic structure of a bot.
- `src`: Contains the scripts that make up the core dialogue management software. 
- `tests`: Contains the files that are used to simulate a conversation with the bots for testing purposes.
  - `tests/test_talk.py`: Script that simulates a continuous conversation with a selected bot. You can call the script from the command line or by using the interpreters of the various IDEs.

Questions & Contact
-------------------
We are still working on creating an extensive documentation on chatbot development by using our framework. Until the documentation is ready, please contact the developers for further information and support.

Paper and Citation
------------------
If you are using our software in your own research, please cite our relevant paper:

ACM style reference:
> Erkan Basar, Divyaa Balaji, Linwei He, Iris Hendrickx, Emiel Krahmer, Gert-Jan de Bruijn, and Tibor Bosse. 2023. [HyLECA: A Framework for Developing Hybrid Long-term Engaging Controlled Conversational Agents.](https://doi.org/10.1145/3571884.3604404) In Proceedings of the 5th International Conference on Conversational User Interfaces (CUI '23). Association for Computing Machinery, New York, NY, USA, Article 56, 1–5. https://doi.org/10.1145/3571884.3604404

BibTeX:

```
@inproceedings{10.1145/3571884.3604404,
    author = {Basar, Erkan and Balaji, Divyaa and He, Linwei and Hendrickx, Iris and Krahmer, Emiel and de Bruijn, Gert-Jan and Bosse, Tibor},
    title = {HyLECA: A Framework for Developing Hybrid Long-term Engaging Controlled Conversational Agents},
    year = {2023},
    isbn = {9798400700149},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3571884.3604404},
    doi = {10.1145/3571884.3604404},
    booktitle = {Proceedings of the 5th International Conference on Conversational User Interfaces},
    articleno = {56},
    numpages = {5},
    keywords = {task-oriented dialogue systems, natural language generation, hybrid conversational agents},
    location = {<conf-loc>, <city>Eindhoven</city>, <country>Netherlands</country>, </conf-loc>},
    series = {CUI '23}
}
```

License
-------
This software is licensed under the GNU General Public License version 3 (GPL v3).