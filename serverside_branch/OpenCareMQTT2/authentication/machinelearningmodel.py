class DTree():
    def __init__(self):
        self.max_depth = 8
        self.left = None
        self.right = None
        self.leaf_val= None
        self.threshval = 1
        self.update_cols = -1

    def get_dict(self,input_vals):
        make_dict = {}
        for entry in input_vals:
            probability = 1.0/float(len(input_vals))
            if entry not in make_dict:
                make_dict[entry] = probability
            else:
                tmp = make_dict[entry]
                make_dict[entry] = tmp+probability
        return make_dict
    def eval_decision_tree(self,field_val):
        if self.leaf_val is not None:
            return self.leaf_val
        
        elif field_val[self.update_cols]>self.threshval:
            return self.right.eval_decision_tree(field_val)
        else:
            return self.left.eval_decision_tree(field_val)