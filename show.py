import matplotlib.pyplot as plt

import re


def gen_list():
    with open('01.xml', 'r', encoding="utf-8") as f:
        text = f.read()
    print(text)
    a = re.findall(r"<TTGlyph name=\"(.*?)\".*?(<contour>.*?)<instructions>.*?</TTGlyph>", text, flags=re.S)
    print(len(a), a)

    for name, str in a:
        x = [int(i) for i in re.findall(r'<pt x="(.*?)" y=', str)]

        y = [int(i) for i in re.findall(r'y="(.*?)" on=', str)]

        print(x)

        print(y)
        plt.axis('off')
        plt.plot(x, y)
        plt.savefig(f'img/{name}.jpg')
        plt.show()


def show():
    str = """
      <contour>
        <pt x="41" y="857" on="1"/>
        <pt x="2036" y="875" on="1"/>
        <pt x="2018" y="674" on="1"/>
        <pt x="42" y="698" on="1"/>
      </contour>
    """

    x = [int(i) for i in re.findall(r'<pt x="(.*?)" y=', str)]

    y = [int(i) for i in re.findall(r'y="(.*?)" on=', str)]

    print(x)

    print(y)
    plt.axis('off')
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    show()
