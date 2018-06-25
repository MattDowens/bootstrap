def convergence_factor(grid):
    key = generate_keys(grid.kmax, grid.lmax, grid.mmax, grid.nmax)[0]
    grid_value = abs(len(grid.allowed_points) - len(grid.disallowed_points))

    convergence = 0
    
    for i in range(len(key)):
        key[i] += 1
        if self.get_grid_index(key) == -1:
            print ("Can't calculate convergence factor. The required grids have not been calculated.")
            break
        else:
            next_grid = self.table[self.get_grid_index(key)]
            next_grid_value = abs(len(next_grid.allowed_points) - len(next_grid.disallowed_points))
            convergence += abs(grid_value - next_grid_value)
        key[i] -= 1
    
    convergence /= len(key)
	return convergence