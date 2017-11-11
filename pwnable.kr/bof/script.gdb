set follow-fork-mode child
break *func+40
commands
    x/40x $esp
    continue
end

run
