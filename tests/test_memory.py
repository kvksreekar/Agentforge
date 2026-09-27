from agentforge.memory import Memory


def test_memory_add_and_trim():
    mem = Memory(max_turns=3)
    for i in range(5):
        mem.add("user", f"msg {i}")
    assert len(mem) == 3
    assert mem.as_messages()[0]["content"] == "msg 2"


def test_memory_clear():
    mem = Memory()
    mem.add("user", "hi")
    mem.clear()
    assert mem.as_messages() == []
    assert len(mem) == 0
