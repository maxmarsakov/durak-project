Ai project - Durak
=======================================

CS 2022 AI project HUJI

Project report is in the repository.

### Play the game vs simple agent:

*python play.py -a human -o simple*

### Play the game vs DQN pretrained agent:

*python durak_rlcard/play.py --model 'model_path'*

For example:
*python durak_rlcard/play.py --model ./experiments/simple_learning_vs_self/model.pth*

Citations:

Zha, Daochen, et al. "RLCard: A Platform for Reinforcement Learning in Card Games." IJCAI. 2020.
```bibtex
@inproceedings{zha2020rlcard,
  title={RLCard: A Platform for Reinforcement Learning in Card Games},
  author={Zha, Daochen and Lai, Kwei-Herng and Huang, Songyi and Cao, Yuanpu and Reddy, Keerthana and Vargas, Juan and Nguyen, Alex and Wei, Ruzhe and Guo, Junyu and Hu, Xia},
  booktitle={IJCAI},
  year={2020}
}
```