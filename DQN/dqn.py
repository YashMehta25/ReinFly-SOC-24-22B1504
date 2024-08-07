import torch
from torch import nn
import torch.nn.functional as F

#Standard way to define a network in PyTorch is by creating a class:
class DQN(nn.Module):

    def __init__ (self, state_dim, action_dim, hiddenlayer_dim = 256) :
        super(DQN, self).__init__()

        self.fc1 = nn.Linear(state_dim, hiddenlayer_dim)
        self.fc2 = nn.Linear(hiddenlayer_dim, action_dim)

    def forward (self, x) :
            x = F.relu(self.fc1(x))
            return self.fc2(x)
        

if __name__ == "__main__":
    state_dim = 12
    action_dim = 2
    net = DQN(state_dim, action_dim)
    state = torch.randn(1, state_dim)
    output = net(state)
    print(output)