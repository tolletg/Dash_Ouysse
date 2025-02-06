{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "58d4d103-577e-47f5-8175-340e19af183b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# run.py\n",
    "from app import app  # Importer l'instance de l'application Dash à partir de app.py\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run_server(debug=True, host='0.0.0.0', port=8080)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
