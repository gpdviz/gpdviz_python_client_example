
You can run this gpdviz client demo as follows:

- Optionally, use [virtualenv](https://virtualenv.pypa.io) to isolate the python 
  environment for this demo, for example:

        $ virtualenv --python=/usr/local/bin/python2.7 virtenv
        $ source virtenv/bin/activate

- Install the [`gpdviz_python_client`](https://github.com/gpdviz/gpdviz_python_client) module:

        $ pip install [--upgrade] git+https://github.com/gpdviz/gpdviz_python_client.git

Then, assuming the target [Gpdviz](https://github.com/gpdviz/gpdviz) server 
is running at `http://localhost:5050`:

- Open [http://localhost:5050/py_demo1/](http://localhost:5050/py_demo1/) in your browser
- Execute:

        $ python demo1.py http://localhost:5050/api
