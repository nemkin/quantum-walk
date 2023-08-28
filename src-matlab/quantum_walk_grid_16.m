n = 4
N = n*n
shift_left = zeros(N,N);
shift_right = zeros(N,N);
shift_down = zeros(N,N);
shift_up = zeros(N,N);

for i=0:N-1
  left = step2d(i, -1, 0, n);
  right = step2d(i, 1, 0, n);
  down = step2d(i, 0, -1, n);
  up = step2d(i, 0, 1, n);
  
  shift_left(left+1, i+1) = shift_left(left+1, i+1) + 1;
  shift_right(right+1, i+1) = shift_right(right+1, i+1) + 1;
  shift_down(down+1, i+1) = shift_down(down+1, i+1) + 1;
  shift_up(up+1, i+1) = shift_up(up+1, i+1) + 1;
end


% S = kron(shift_up, [1,0,0,0]' * [1,0,0,0]) + ...
% kron(shift_right, [0,1,0,0]' * [0,1,0,0]) + ...
% kron(shift_down, [0,0,1,0]' * [0,0,1,0]) + ...
% kron(shift_left, [0,0,0,1]' * [0,0,0,1]);

S = kron(shift_up * shift_left, [1,0,0,0]' * [1,0,0,0]) + ...
kron(shift_up * shift_right, [0,1,0,0]' * [0,1,0,0]) + ...
kron(shift_down * shift_left, [0,0,1,0]' * [0,0,1,0]) + ...
kron(shift_down * shift_right, [0,0,0,1]' * [0,0,0,1]);

shift_up
shift_down
shift_left
shift_right
S

I = eye(N)

H = [1,1,1,1; 1,-1,1,-1; 1,1,-1,-1; 1,-1,-1,1] / 2;
%G = [0,1;1,0];
G = [-1,1,1,1; 1,-1,1,1; 1,1,-1,1; 1,1,1,-1] / 2;
C = G

Chat = kron(I, C)

SC = S * Chat

l = eig(SC)
