pip install tasks


main='https://raw.githubusercontent.com/radcool510/majora-mask-bot/main/bot/main.py'




function looper () {
    while true
    do
        python3 $main $@
    done

looper
