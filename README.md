# IT3105-MCTS

State Manager documentation:  
__\_\_init\_\_()__  
@params whatever parameters it needs  

__get_start()__  
@return position: starting position  

__get_child_state_keys()__  
@param state_key: key of a state  
@return states, moves: reachable states and corresponding moves from state_key  

__winner()__  
@param state_key: key of state  
@return int: 0 if no winner, 1 or 2 if state is a win for corresponding player  
