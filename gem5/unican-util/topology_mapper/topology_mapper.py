#
#  Copyright (c) 2015-2020 University of Cantabria
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met: redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer;
#  redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution;
#  neither the name of the copyright holders nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Authors: Ivan Perez
#

concentration = [2,2]
booksim_mesh = [8,8]

nodes = 1
for x in concentration:
    nodes = nodes * x
for x in booksim_mesh:
    nodes = nodes * x

num_dirs = 4
num_l1 = 64
num_l2 = 64

l1 = []
l2 = []

i_pointer = 0
j_pointer = 0
for j in range(booksim_mesh[1]):
    for i in range(booksim_mesh[0]):
        l1.append(i_pointer+j_pointer)
        l2.append(i_pointer+j_pointer+1)
        i_pointer = i_pointer + concentration[0]
    i_pointer = 0
    j_pointer = concentration[1] * concentration[0] * booksim_mesh[0] +\
            j_pointer

dirs = [booksim_mesh[0]*concentration[0],
        2*booksim_mesh[0]*concentration[0]-1,
        nodes-2*booksim_mesh[0]-1,nodes-1]

print("L1 id: ",l1, " length: ", len(l1), "\nL2 id: ", l2, " length: ",
        len(l2), "\nDir id: ", dirs, " length: ", len(dirs))
