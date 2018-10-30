# IT3105-MCTS

State Manager documentation  
__init__()  
@params whatever parameters it needs  

get_start()  
@return position: starting position  

get_child_state_keys()  
@param state_key: key of a state  
@return states, moves: reachable states and corresponding moves from state_key  

winner()  
@param state_key: key of state  
@return int: 0 if no winner, 1 or 2 if state is a win for corresponding player  
