from Player import ComputerPlayer, HumanPlayer
from board import Hash
from state.state import State
import datetime

if __name__ == '__main__':
    hash = Hash()
    p1 = ComputerPlayer("p1", hash)
    p2 = ComputerPlayer("p2", hash)
    model = ComputerPlayer("model", hash, exp_rate=0)
    st = State(p1, p2, hash)
    try:
        p1.loadPolicy("model_.p1")
        p2.loadPolicy("model_.p2")
        model.loadPolicy("h5_.model")
        # print(len(p1.q_value))
        # print(len(p2.q_value))
    except:
        print("Computer needs some training...\n")
        t1 = datetime.datetime.now()
        for i in range(50):
            st.train(500)
            print(p1.exp_rate)
            if len(p2.q_value) + len(p1.q_value) == 764:
                p1.exp_rate = 0.1
                p2.exp_rate = 0.1
        t2 = datetime.datetime.now()
        print(t2-t1)
        p1.savePolicy()
        p2.savePolicy()
        model.saveTrainedModel(p1.q_value, p2.q_value)

        print("Done training it's time to play a human\n")
        print(len(p1.q_value) + len(p2.q_value))


    human = HumanPlayer("human")
    st = State(model, p2, hash)
    st.play()