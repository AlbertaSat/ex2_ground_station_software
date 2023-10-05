#!/bin/bash

session="ops_primary"

tmux new-session -d -s $session

tmux rename-window -t $session:1 'ops primary'
tmux split-window -v
tmux split-window -v
tmux select-layout even-vertical
tmux split-window -h

tmux new-window -t $session:2 -n 'background processes'
tmux split-window -h
tmux select-pane -t $session:2.1
tmux split-window -v -p 10

tmux select-window -t $session:1


