from di.di import Profile


class TestProfile:
    class Test_生成について:
        def test_プロファイル値指定でProfileを生成できる(self):
            Profile({'A', 'B'})
