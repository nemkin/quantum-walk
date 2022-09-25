S_0 = [
    0,0,0,0,1;
    0,0,0,0,0;
    0,0,0,0,0;
    0,0,1,0,0;
    1,1,0,1,0]

S_1 = [
    0,0,1,1,0;
    0,1,0,0,0;
    0,0,0,0,0;
    1,0,0,0,1;
    0,0,0,0,0]

S_2 = [
    0,0,0,0,0;
    0,0,0,1,1;
    1,1,1,0,0;
    0,0,0,0,0;
    0,0,0,0,0]

S_3 = [
    1,0,0,0,0;
    0,1,0,0,0;
    0,0,1,0,0;
    0,0,0,1,0;
    0,0,0,0,1;
    ]

o_0 = [1; 0; 0; 0]
o_1 = [0; 1; 0; 0]
o_2 = [0; 0; 1; 0]
o_3 = [0; 0; 0; 1]

S = kron(o_0*o_0',S_0) + kron(o_1*o_1',S_1) + kron(o_2*o_2',S_2) + kron(o_3*o_3',S_3)


S'
inv(S)