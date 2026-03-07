@echo off
echo Starting the 125M LLM...
echo.

call .venv\Scripts\activate

python llm.py %*

echo.
echo Done.
pause 
