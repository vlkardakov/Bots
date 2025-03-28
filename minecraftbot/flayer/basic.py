from javascript import require, On
import time

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
pvp = require('mineflayer-pvp').plugin
armor_manager = require('mineflayer-armor-manager')

BOT_USERNAME = 'python'
WATCHED_PLAYER = 'vlkardakov'  # Игрок, за которым следим
RANGE_GOAL = 10

bot = mineflayer.createBot({
    'host': '87.120.187.59',
    'port': 25565,
    'username': BOT_USERNAME
})

bot.loadPlugin(pathfinder.pathfinder)
bot.loadPlugin(pvp)
bot.loadPlugin(armor_manager)

print("Бот запущен")


@On(bot, 'spawn')
def on_spawn(*args):
    print("Бот появился")
    bot.chat('Я появился!')
    bot.movements = pathfinder.Movements(bot)
    bot.pathfinder.setMovements(bot.movements)
    bot.pathfinder.setGoal(None)
    bot.controlState.sprint = True


import time
# Assuming javascript, mineflayer, pathfinder, Vec3 etc. are imported correctly
# Assuming WATCHED_PLAYER and RANGE_GOAL are defined somewhere

@On(bot, 'chat')
def on_chat(this, username, message, *args):
    if username != WATCHED_PLAYER:
        return

    parts = message.lower().split()
    if not parts or parts[0] != "attack":
        return

    if len(parts) < 2:
        bot.chat("Укажи цель: attack <username>")
        return

    target_username = parts[1]
    if target_username == 'enemy': target_username = 'javascript'
    bot.chat(f"Принято, атакую {target_username}")

    target_player = bot.players[target_username] # Use .get() for safer dictionary access
    attack_mob = False
    if not target_player:

        bot.chat(f'Не вижу игрока с ником {target_username}, ищу моба')

        potential_entities = list(entity for entity in bot.entities.values() if entity.name == target_username)
        if min(
            potential_entities,
            key=lambda entity: bot.entity.position.distanceTo(entity.position),
            default=None
        ):
            bot.chat('Найден!!')
            attack_mob = True
        else:
            print(f"Player '{target_username}' not found in bot.players.")
            # Optional: print available players for debugging
            # print("Available players:", list(bot.players.keys()))
            return

    print(f'Цель найдена: {target_username}')

    # --- Check if the player has a valid entity ---
    target_entity = target_player.entity
    if not target_entity:
        bot.chat(f"Я вижу игрока {target_username}, но не могу получить его сущность! Возможно, он слишком далеко.")
        print(f"Entity not found for player '{target_username}'. Player object: {target_player}")
        return

    print(f'Сущность цели найдена (ID: {target_entity.id})')

    # --- Pathfinding ---
    bot.pathfinder.setGoal(pathfinder.goals.GoalFollow(target_entity, RANGE_GOAL))
    print('Путь задан')

    # --- Attack Loop ---
    # WARNING: This blocking `while True` loop with `time.sleep` is generally
    # not recommended in asynchronous environments like Mineflayer/Node.js.
    # It can block other bot events. A better approach would use events
    # or async functions if the Python wrapper supports them well.
    # For this example, we'll keep it similar but add checks.

    attack_attempts = 1
    MAX_ATTEMPTS = 2000 # Add a limit to prevent infinite loops if something goes wrong

    while attack_attempts < MAX_ATTEMPTS:

        # Re-check if target is still valid and nearby in each iteration
        current_target_player = bot.players[target_username]
        if not current_target_player or not current_target_player.entity or not current_target_player.entity.isValid:
            bot.chat(f"Готово!")
            print(f"Target {target_username} lost or entity became invalid.")
            bot.pathfinder.stop() # Stop following if target is lost
            break

        if attack_mob:
            potential_entities = list(entity for entity in bot.entities.values() if entity.name == target_username)
            target_entity = min(
                    potential_entities,
                    key=lambda entity: bot.entity.position.distanceTo(entity.position),
                    default=None
            )

        else:
            target_entity = current_target_player.entity

        sword = next((item for item in bot.inventory.items() if "sword" in item.name.lower()), None)
        if sword:
            try:
                # Avoid equipping if already holding it
                if bot.heldItem is None or bot.heldItem.type != sword.type:
                    print(f"Экипирую {sword.name}")
                    bot.equip(sword, "hand")
                    # It might be wise to wait a tiny bit after equipping
                    time.sleep(0.2)
            except Exception as e:
                print(f"Ошибка при экипировке меча: {e}")
                # Decide whether to proceed without sword or stop

        # --- Attack ---
        print(f'Атакую {target_username} (Сущность ID: {target_entity.id})')
        try:
            # *** THE FIX: Pass the entity object ***
            bot.pvp.attack(target_entity)
            print("Атака отправлена.")
            attack_attempts += 1
        except Exception as e:
            print(f"Ошибка во время вызова bot.pvp.attack: {e}")
            # Consider breaking the loop if attacks consistently fail
            bot.pathfinder.stop()
            break

        # --- Wait ---
        # Adjust sleep time based on attack speed/cooldown. 2 seconds might be too long.
        attack_cooldown = 1.0 # Example cooldown
        print(f"Жду {attack_cooldown} сек...")
        time.sleep(attack_cooldown)

    if attack_attempts >= MAX_ATTEMPTS:
        print("Достигнут лимит попыток атаки.")
        bot.chat(f"Завершаю атаку на {target_username} (лимит попыток).")

    # Ensure pathfinder stops after the loop finishes or breaks
    bot.pathfinder.stop()
    print("Цикл атаки завершен.")
