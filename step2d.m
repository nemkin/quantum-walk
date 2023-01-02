function ret = step2d(i, stepx, stepy, n)
  i_x = mod(i,n);
  i_y = floor(i/n);
  
  ret_x = mod(i_x+stepx, n);
  ret_y = mod(i_y+stepy, n);
  ret = ret_y * n + ret_x;
end
