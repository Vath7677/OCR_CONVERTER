

# this is a cmd line that was use to run when start the new terminal 


conda deactivate

# active venv
source .venv/bin/activate

# run backend
uv run uvicorn app.main:app --reload

# run fronted
uv run python -m http.server 3000 --directory frontend



# docker

# use to build a container
docker build -t ocr-converter .

# run app
docker run -p 7860:7860 ocr-converter

# when u have chnage a code in docker after we build alrady u need to run this one to make a docker update code 
docker run -p 7860:7860 -v $(pwd):/app ocr-converter