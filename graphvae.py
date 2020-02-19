import dgl

class NodeApplyModule(nn.Module):
    def __init__(self, in_feats, out_feats, activation):
        super(NodeApplyModule, self).__init__()
        self.linear = nn.Linear(in_feats, out_feats)
        self.activation = activation
     
    def forward(self, node):
        h = self.linear(node.data['h'])
        h = self.activation(h)
        return {'h': h}

class GCN(nn.Module):
    def __init__(self, in_feats, out_feats, activation):
        super(GCN, self).__init__()
        self.apply_mod = NodeApplyModule(in_feats, out_feats, activation)
     
    def forward(self, g, feature):
        g.ndata['h'] = feature
        g.update_all(gcn_msg, gcn_reduce)
        g.apply_nodes(func=self.apply_mod)
        h =  g.ndata.pop('h')
        return h

class GAE(nn.Module):
    def __init__(self, in_dim, hidden_dims):
        super(GAE, self).__init__()
        layers = [GCN(in_dim, hidden_dims[0], F.relu)]
        if len(hidden_dims)>=2:
            layers = [GCN(in_dim, hidden_dims[0], F.relu)]
            for i in range(1,len(hidden_dims)):
                if i != len(hidden_dims)-1:
                    layers.append(GCN(hidden_dims[i-1], hidden_dims[i], F.relu))
                else:
                    layers.append(GCN(hidden_dims[i-1], hidden_dims[i], lambda x:x))
        else:
            layers = [GCN(in_dim, hidden_dims[0], lambda x:x)]
        self.layers = nn.ModuleList(layers)
        self.decoder_adj = InnerProductDecoder(activation=lambda x:x)
        self.decoder_props = LSTM_Mod(activation=lambda x:x)
    
    def forward(self, g):
        h = g.ndata['h']
        for conv in self.layers:
            h = conv(g, h)
        g.ndata['h'] = h
        adj_rec = self.decoder_adj(h)
        props = self.decoder_props(h, len(g.nodes))
        return adj_rec

    def encode(self, g):
        h = g.ndata['h']
        for conv in self.layers:
            h = conv(g, h)
        return h

class LSTM_Mod(nn.Module):
	def __init__(self, dropout = 0.1, batch = 32, input_dim = 500, n_layers = 3, n_toks = 5, hidden_dim = 100):
		self.dropout = dropout
		self.lstm = nn.LSTM(input_dim, hidden_dim, n_layers, batch_first=True)
		h_0 = nn.Variable(num_layers, batch, hidden_dim)
	def forward(self, h):
		h_size = torch.cat([h]*n_toks).view(n_toks, batch, input_dim)
		out, hidden = lstm_layer(h_size, h_0)
		out = (out[:,:,:15], out[:,:,15], out[:,:,16])
		out = (nn.Softmax(out[0]), out[1], out[2])
		return out

class InnerProductDecoder(nn.Module):
    def __init__(self, activation=torch.sigmoid, dropout=0.1):
        super(InnerProductDecoder, self).__init__()
        self.dropout = dropout
        self.activation = activation

    def forward(self, z):
        z = F.dropout(z, self.dropout)
        adj = self.activation(torch.mm(z, z.t()))
        return adj

def lossFunction(out, correct_out):
	return 50*nn.MSELoss(out[0], correct_out[0]) + 10*nn.MSELoss(out[1], correct_out[1]) + 10*nn.MSELoss(out[2], correct_out[2])