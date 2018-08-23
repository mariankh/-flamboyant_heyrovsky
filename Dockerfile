# nvidia-docker build -t rosindustrial/ros-core-nvidia:lunar .
FROM nvidia/cuda:8.0-devel-ubuntu16.04
LABEL maintainer "Austin.Deric@SwRI.org"

# setup keys
RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    && rm -rf /var/lib/apt/lists/*

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

# install ros packages
ENV ROS_DISTRO lunar
RUN apt-get update && apt-get install -y \
    ros-lunar-ros-core \
    && rm -rf /var/lib/apt/lists/*

# setup entrypoint
#COPY ./ros_entrypoint.sh /

#ENTRYPOINT ["/ros_entrypoint.sh"]
#CMD ["bash"]

# Use an official Python runtime as a parent image
FROM python:2.7-slim
RUN apt-get update && apt-get install -y python-pip

# Make port 80 available to the world outside this container
EXPOSE 80

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
