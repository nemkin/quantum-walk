lineS0 = [0,1,0,0; 0,0,1,0; 0,0,0,1; 1,0,0,0]
lineS1 = [0,0,0,1; 1,0,0,0; 0,1,0,0; 0,0,1,0]

lineR0 = [1, 0; 0, 0]
lineR1 = [0, 0; 0, 1]

lineS = kron(lineS0, lineR0) + kron(lineS1, lineR1) 

lineI = eye(4)

lineH = [1,1;1,-1] / sqrt(2);
lineG = [0,1;1,0];
lineC = lineG

lineChat = kron(lineI, lineC)

lineSC = lineS * lineChat

linel = eig(lineSC)
