for ((id=56200; id <= 56220; id++))
do
    echo
    echo $id
    curl  --cookie "miden=jsecl7o0isa52nk9gtfl9jl4es" "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie_all.php?schet=205.2425%2F1&type_z=1&faculty=57185&kurs=2&group=$id" --user-agent "Teste" | iconv --from-code WINDOWS-1251 --to-code UTF-8 | grep группы
done
