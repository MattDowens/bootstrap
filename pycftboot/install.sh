#!/bin/bash -e
#
# This script installs all of the dependencies for pycftboot locally into
# your home directory, making them avaiable for you to use everywhere on
# the School Linux platform, including the School Compute Cluster.
#
# It also demonstrates a local run of pycftboot, though it's not totally
# clear how you'd do a "proper" install of pycftboot! See below for details.

BUILD_DIR=/tmp/I180712-0576
mkdir -p $BUILD_DIR

# We'll install into ~/.local, which is a semi-standardish
# location for installing things locally
INSTALL_DIR=~/.local
mkdir -p $INSTALL_DIR

########################################################################
# Dependencies

# Download, build and install Symengine
cd $BUILD_DIR
wget https://github.com/symengine/symengine/archive/v0.3.0.tar.gz -O symengine-0.3.0.tar.gz
tar zxf symengine-0.3.0.tar.gz
cd symengine-0.3.0
cmake -DCMAKE_INSTALL_PREFIX:PATH=$INSTALL_DIR -DWITH_MPFR:BOOL=ON
make && make install

# Download, build and install Symengine.py
# NB: Building only Python 2 bindings for now as pycftboot is Python 2
cd $BUILD_DIR
wget https://github.com/symengine/symengine.py/archive/v0.3.0.tar.gz -O symengine.py-0.3.0.tar.gz
tar zxf symengine.py-0.3.0.tar.gz
cd symengine.py-0.3.0
python2 setup.py install --user build_ext --symengine-dir=$INSTALL_DIR

# Download, build and install SDPB
cd $BUILD_DIR
wget https://github.com/davidsd/sdpb/archive/v1.0.tar.gz -O sdpb-1.0.tar.gz
tar zxf sdpb-1.0.tar.gz
cd sdpb-1.0
sed -i -e 's|/usr/local|/usr|g' Makefile
make
mkdir -p $INSTALL_DIR/bin
cp sdpb $INSTALL_DIR/bin

########################################################################

# pycftboot stuff
# TODO: It's not obvious how/where this should get installed...
# The bootstrap.py file reads in various other files using open(),
# and it seems they need to be in the current directory.
# So the only way I could get this working is to run my stuff from
# the same directory as bootstrap.py et al...
#
cd $BUILD_DIR
rm -rf pycftboot
git clone https://github.com/cbehan/pycftboot.git
cd pycftboot
# Need to hard-code the path to the SDPB binary
sed -i -e "/sdpb_path =/c sdpb_path = \"$INSTALL_DIR/bin/sdpb\"" common.py

########################################################################
# Things you need to do to run stuff

# Do the following if you want to run SDPB directly.
# It's not needed if you're just using pycftboot as that hard-codes
# the path to SPDB (see above)
export PATH=$INSTALL_DIR/bin:$PATH

# Probably need to be in the same directory as all of the pycftboot files
cd $BUILD_DIR/pycftboot

# Test!
python2 tutorial.py
