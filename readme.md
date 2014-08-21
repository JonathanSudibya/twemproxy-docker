# Twemproxy Docker!
This docker image contains twemproxy configured to run standalone with
two bundled memcached instances or memcached instanced dynamically
looked up via EC2 instance tags. 

## Running It

```bash

docker run -d -p 22121:22121 -p 22222:22222 jamescarr/nutcracker-embedded

```

Now you should be able to point any run of the mill memcached client at
it on port 22121 and start using it. 

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
  jamescarr/nutcracker-embedded


```

This will collect all EC2 instances tagged with role=cache and populate
the backend list with private IP addresses. 

## Building It
A token vagrant box is provided for those who do not have a native
vagrant environment. 

```bash
sudo docker build . # seriously were you expecting more???
```

* `generate_configs.py` - python script that generates supervisor and
twemproxy (nutcracker) configurations dynamically
* `run.sh` - shell script to run generate_configs.py followed by
supervisor. Runs by default when starting the container.


