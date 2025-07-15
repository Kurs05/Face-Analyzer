
# Face-Analyzer using Dlib and DeepFace

This project detects human emotions from facial expressions using DeepFace, draws facial landmarks on the image using the dlib library, and stores the results in a local SQLite database. Note that the analysis results may contain inaccuracies, as no AI system is perfect.




https://github.com/user-attachments/assets/371c5e94-55b6-47eb-9a22-b14b03802cad





## Technologies Used

- Python 3.10 (with newer versions, it may not work!)
- Django 5.2.4
- OpenCV – for image preprocessing (optional, but useful)
- DeepFace - for facial analysis and emotion detection
- Dlib - for detection landmarks
- SQLite - to store results in real-time



## Installation

1) Clone the repository
2) Set up a virtual environment (recommended)
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
3) Install dependencies 
```bash
pip install -r requirements.txt
```
 If the terminal prompts you to install a library, make sure to install it as well.

4) Run Django server 
```bash
py manage.py runserver
```
5) Registration is required! Alternatively, you can log in using the admin credentials (email: [admin@gmail.com](mailto:admin@gmail.com), password: 123123).


## Screenshots

<img width="1826" height="924" alt="image_2025-07-14_18-09-42" src="https://github.com/user-attachments/assets/26a242e1-d25e-4fdf-a057-32a237ab7e9c" />

<img width="1855" height="918" alt="image_2025-07-14_18-10-56" src="https://github.com/user-attachments/assets/0426d488-66e9-4d6c-a8f5-1fa302703a1b" />

<img width="1489" height="793" alt="image_2025-07-14_18-11-06" src="https://github.com/user-attachments/assets/459fca0f-deff-4a8d-9887-75416737268a" />

<img width="1820" height="922" alt="image_2025-07-14_18-11-13" src="https://github.com/user-attachments/assets/25716754-8c2c-4b6b-8057-e621fe2d37fc" />


Feel free to fork, modify, and submit a pull request. Happy coding!
