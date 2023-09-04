pip install tasks
pip install openai


main='https://raw.githubusercontent.com/radcool510/majora-mask-bot/main/bot/main.py'



#
# this will keep running the bot
#
function looper () {
    while true
    do
        python3 $main $@
    done

looper
