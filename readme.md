# Twemproxy Docker!
This docker image contains twemproxy configured to run standalone with
two bundled memcached instances or memcached instances dynamically
looked up via EC2 instance tags. 

## Running It

```bash

docker run -d -p 22121:22121 -p 22222:22222 zapier/twemproxy

```

Now you should be able to point any run of the mill memcached client at
it on port 22121 and start using it. 

There is already a tiny test suit that runs in a docker container to test the connectivity with twemproxy. To run it, you need to run the twemproxy container:

```
sudo docker run --name nutcracker -d -p 22121:22121 -p 22222:22222 zapier/twemproxy

```

You'll also need to cd to the test directory of the repository and built the test docker image:

```
sudo docker build -t memcache_test .
```

Once that is done, you can run the test container by linking the nutcracker container.

```
sudo docker run --link nutcracker:proxy --name test --rm memcache_test

```

If all goes well, you should see some passing tests!

![](http://i.imgur.com/NqjCRIN.png)

### AWS Support

You can swap out the embedded backends for real backends on EC2 by
defining a series of environment variables to define what instances to
use as backends based on tags. 

```bash

docker run -d \
  -p 22121:22121 -p 22222:22222 \
  -e AWS_TAG_NAME=role \
  -e AWS_TAG_VALUE=cache \
  -e AWS_PUBLIC_IP=false \
  zapier/twemproxy


```

This will collect all EC2 instances tagged with role=cache and populate
the backend list with private IP addresses. 

## Building It
A token vagrant box is provided for those who do not have a native
docker environment. 

```bash
sudo docker build . # seriously were you expecting more???
```

* `generate_configs.py` - python script that generates supervisor and
twemproxy (nutcracker) configurations dynamically
* `run.sh` - shell script to run generate_configs.py followed by
supervisor. Runs by default when starting the container.


