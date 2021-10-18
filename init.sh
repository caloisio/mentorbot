PY=$(case $(uname -s) in
    Drawin* | Linux* ) echo "python";;
    * ) echo "py";;
esac)

echo "Welcome to the automated Mentorbot installer, please ensure that python is installed"
read -p "Press enter to continue"

echo "creating python venv..."
$PY -m venv ./.venv

echo "sourcing new venv..."
case $(uname -s) in
    Darwin* | Linux*) # https://docs.python.org/3/tutorial/venv.html
        source ./.venv/bin/activate;;
    *)
        source ./.venv/Scripts/activate;;
esac

echo "installing robotpy..."
$PY -m pip install -U robotpy[all]

echo "complete!"

