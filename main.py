from src import Tokenizer, Parser


def main() -> None:
    tokenizer: Tokenizer = Tokenizer(r"int one_3hello0::tconstwo<mytemplate>::three(const four &) volatile")
    for tok in tokenizer.get_all_tokens():
        print(tok)

    fqn = (r"test1::test2< T *> "
           r"one_3hello0::tconstwo< mytemplate>::three<Test::type<T * >::Hello>"
           r"(const four &, int a) volatile")
    parser = Parser(fqn)
    parsed_fqn = parser.parse()
    print(parsed_fqn)


if __name__ == '__main__':
    main()
