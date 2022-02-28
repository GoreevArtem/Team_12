<div align="center">

# Bot for colonizing photos (Team 12)

![Python](https://img.shields.io/badge/-Python-000000?style=for-the-badge&logo=Python&logoColor=39E830) ![Tensorflow](https://img.shields.io/badge/-Tensorflow-000000?style=for-the-badge&logo=Tensorflow&logoColor=DF3C34) ![Keras](https://img.shields.io/badge/-Keras-000000?style=for-the-badge&logo=Keras&logoColor=fb031f) ![MongoDB](https://img.shields.io/badge/-MongoDB-000000?style=for-the-badge&logo=MongoDB&logoColor=52ff6a) ![Docker](https://img.shields.io/badge/-Docker-000000?style=for-the-badge&logo=Docker&logoColor=1b8dff)

Telegram bot project for coloring black and white photos with the ability to save them both on the user's side and on the server side
</div>

--- 
## Our team
    Mikhail Extrin (QA) 

    Goreev Artoym (Team Leader)
---

## Getting Started

### System requirements
Linux / Windows

python 3.7 and higher

### Clone Repository
```
git clone https://github.com/nn-students-2021h2/Colorization_of_photos_12.git
cd Colorization_of_photos_12/
```

### Requirements
```
pip install -r requirements.txt
```

### Download the dataset
Download dataset and place it in the `/DATASET/` folder.
You can download it from <a href="http://image-net.org/download"> here </a> 

---
## How to use

Our bot named <b>"Color bot"</b> in Telegram

Then start a conversation with the bot to check if it is activated.

If you want to use your bot token, then:

1) Clone this repository
2) Create Telegram bot <a href="https://core.telegram.org/bots#6-botfather"> Telegram instructions </a>
3) Put your token in the `TOKEN' variable in the json file
4) Install [MongoDB](https://www.mongodb.com/try/download/community)
5) After that you can use the bot


---
## Additional Resources
### Run inferences using Docker

You can colorize arbitrary grayscale images using a pre-packaged Docker image from the Replicate registry: <a href="#"> here </a> 

---

## Resources
* [coloring photos a trained model](https://github.com/pvitoria/ChromaGAN)
