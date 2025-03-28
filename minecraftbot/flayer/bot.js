const mineflayer = require('mineflayer');
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder');
const {goals: { GoalNear } } = require('mineflayer-pathfinder')
const collectBlock = require('mineflayer-collectblock').plugin
const { plugin: pvp } = require('mineflayer-pvp');
const armorManager = require('mineflayer-armor-manager');

const BOT_USERNAME = 'javascript';
const WATCHED_PLAYER = 'vlkardakov'; // Игрок, за которым следим
const RANGE_GOAL = 3;
let protectedPlayer = null;
let following = false;

const bot = mineflayer.createBot({
    host: '87.120.187.59',
    port: 25565,
    username: BOT_USERNAME
});

bot.loadPlugin(pathfinder);
bot.loadPlugin(pvp);
bot.loadPlugin(armorManager);
bot.loadPlugin(collectBlock);

let mcData
let miningSand = false

console.log("Бот запущен");

const { GoalFollow } = goals;
const vec3 = require('vec3'); // Required for vector math used in raycasting
let followingProtectedPlayer = false;

async function collectBlockType(blockName, count) {
  let collected = 0

  async function mineNext() {
    if (collected >= count) {
      bot.chat(`Добыто ${collected} блоков ${blockName}`)
      miningSand = false
      return
    }

    const block = bot.findBlock({
      matching: mcData.blocksByName[blockName]?.id,
      maxDistance: 64
    })

    if (block) {
      try {
        await bot.collectBlock.collect(block)
        collected++
        mineNext()
      } catch (err) {
        bot.chat(`Ошибка добычи: ${err.message}`)
        miningSand = false
      }
    } else {
      bot.chat(`Блок ${blockName} не найден`)
      miningSand = false
    }
  }

  mineNext()
}


bot.on('spawn', () => {
    mcData = require('minecraft-data')(bot.version)
    console.log("Бот появился");
    bot.chat('Я появился!');
    bot.movements = new Movements(bot);
    bot.pathfinder.setMovements(bot.movements);
    bot.pathfinder.setGoal(null);
    bot.controlState.sprint = true;
});

bot.on('chat', (username, message) => {
    if (username !== WATCHED_PLAYER) return;

    const parts = message.toLowerCase().split(" ");
    if (parts[0] === "attack" && parts.length >= 2) {
        let targetUsername = parts[1];
        if (targetUsername === 'enemy') targetUsername = 'javascript';
        bot.chat(`Принято, атакую ${targetUsername}`);

        let targetPlayer = bot.players[targetUsername]?.entity;
        if (!targetPlayer) {
            bot.chat(`Не вижу игрока с ником ${targetUsername}, ищу моба`);
            targetPlayer = bot.nearestEntity(entity =>
  (entity.username && entity.username === targetUsername) ||
  (entity.mobType && entity.mobType === targetUsername) ||
  (entity.name && entity.name === targetUsername) ||
  (entity.displayName && entity.displayName === targetUsername) ||
  (entity.entityType && entity.entityType.toString() === targetUsername) ||
  (entity.kind && entity.kind === targetUsername)
);

            if (!targetPlayer) {
                bot.chat(`Не найден моб ${targetUsername}`);
                return;
            }
        }

        bot.chat(`Цель найдена: ${targetUsername}`);
        bot.pathfinder.setGoal(new goals.GoalFollow(targetPlayer, RANGE_GOAL));

        let attackAttempts = 0;
        const MAX_ATTEMPTS = 2000;

        function attackLoop() {
            if (!targetPlayer || !targetPlayer.isValid) {
                bot.chat("Готово!");
                bot.pathfinder.setGoal(null);
                return;
            }

            const sword = bot.inventory.items().find(item => item.name.includes("sword"));
            if (sword && (!bot.heldItem || bot.heldItem.type !== sword.type)) {
                bot.equip(sword, 'hand').catch(err => console.log(`Ошибка при экипировке меча: ${err}`));
            }

            bot.pvp.attack(targetPlayer);
            console.log(`Атакую ${targetUsername}`);
            attackAttempts++;

            if (attackAttempts < MAX_ATTEMPTS) {
                setTimeout(attackLoop, 1000);
            } else {
                bot.chat(`Завершаю атаку на ${targetUsername} (лимит попыток).`);
                bot.pathfinder.setGoal(null);
            }
        }

        attackLoop();
    }

  if (parts[0] === "mine" && parts.length === 3) {
    const blockType = parts[1]
    const amount = parseInt(parts[2])

    if (!mcData.blocksByName[blockType]) {
      bot.chat(`Неизвестный блок: ${blockType}`)
      return
    }

    if (isNaN(amount) || amount <= 0) {
      bot.chat("Неправильное количество")
      return
    }

    if (miningSand) {
      bot.chat("Я уже копаю, подожди!")
      return
    }

    miningSand = true
    collectBlockType(blockType, amount)
  }


    if (parts[0] === "kill" && parts.length >= 2) {
        let targetUsername = parts[1];
        if (targetUsername.toLowerCase() === 'enemy') targetUsername = 'zombie';

        bot.chat(`Ищу видимую цель: ${targetUsername}`);

        // Function to check line of sight using raycasting
        function isEntityVisible(entity) {
            if (!entity) return false;
            const botEyePosition = bot.entity.position.offset(0, bot.entity.height, 0);
            const targetHeadPosition = entity.position.offset(0, entity.height, 0); // Aim for the head/upper body
            const distance = botEyePosition.distanceTo(targetHeadPosition);

            // Avoid raycasting towards self or entities that are too far away
            if (entity === bot.entity || distance > 128) { // Adjust max distance if needed
                 return false;
            }

            const direction = targetHeadPosition.subtract(botEyePosition).normalize();

            try {
                const blockHit = bot.world.raycast(botEyePosition, direction, distance, (block) => {
                     // Consider transparent blocks as not obstructing vision for simplicity,
                     // adjust if you need stricter checks (e.g., block.boundingBox === 'empty')
                     return block.boundingBox !== 'empty' && !block.name.includes('glass') && !block.name.includes('leaves'); // Example: ignore glass/leaves
                 });

                // If raycast hit null (nothing solid in the way) or hit the entity itself, it's visible
                // Note: Raycast doesn't directly return the entity hit in this overload, only the block.
                // So, if blockHit is null, it means the path is clear up to the target's distance.
                return blockHit === null;

            } catch (e) {
                // Catch potential errors during raycasting (though less common now)
                console.error(`Raycast error when checking visibility for ${entity.username || entity.name || entity.mobType}:`, e);
                return false;
            }
        }


        // Use bot.nearestEntity with a filter that checks BOTH matching criteria AND visibility via raycast
        const targetEntity = bot.nearestEntity(entity => {
            // 1. Check if the entity matches the target name/type (case-insensitive)
            const nameLower = targetUsername.toLowerCase();
            const matchesCriteria = (
                (entity.type === 'player' && entity.username?.toLowerCase() === nameLower) ||
                (entity.type === 'mob' && entity.mobType?.toLowerCase() === nameLower) ||
                (entity.name?.toLowerCase() === nameLower) ||
                (entity.displayName?.toLowerCase() === nameLower)
            );

            if (!matchesCriteria) {
                return false; // Doesn't match the name/type
            }

            // 2. Check if the matching entity is visible using raycast
            return isEntityVisible(entity);
        });

        if (!targetEntity) {
            bot.chat(`Не вижу сущность с именем/типом ${targetUsername}.`);
            return;
        }
        const targetName = targetEntity.username || targetEntity.mobType || targetEntity.name || 'неизвестная сущность';
        bot.chat(`Видимая цель найдена: ${targetName}`);

        bot.pathfinder.setGoal(new goals.GoalFollow(targetEntity, RANGE_GOAL));

        let attackAttempts = 0;
        const MAX_ATTEMPTS = 2000;

        function attackLoop() {
            if (!targetEntity || !targetEntity.isValid) {
                bot.chat("Готово!");
                bot.pathfinder.setGoal(null);
                return;
            }

            const sword = bot.inventory.items().find(item => item.name.includes("sword"));
            if (sword && (!bot.heldItem || bot.heldItem.type !== sword.type)) {
                bot.equip(sword, 'hand').catch(err => console.log(`Ошибка при экипировке меча: ${err}`));
            }

            if (isEntityVisible(targetEntity)) {
                bot.pvp.attack(targetEntity);
                console.log(`Атакую!`);
                attackAttempts++;
            } else {
                bot.chat('Не вижу! :(')
//                bot.pvp.stop()
            }


            if (attackAttempts < MAX_ATTEMPTS) {
                setTimeout(attackLoop, 1000);
            } else {
                bot.chat(`Завершаю атаку (лимит попыток).`);
                bot.pathfinder.setGoal(null);
                bot.pvp.stop()
            }
        }

        attackLoop();
    }


    else if (parts[0] === "nearest" && parts.length >= 2) {
        let entityType = parts[1];
        let nearestEntity = Object.values(bot.entities)
            .filter(entity => entity.name === entityType || entity.type === entityType)
            .reduce((nearest, entity) => {
                if (!nearest || bot.entity.position.distanceTo(entity.position) < bot.entity.position.distanceTo(nearest.position)) {
                    return entity;
                }
                return nearest;
            }, null);

        if (nearestEntity) {
            bot.chat(`Ближайшая сущность: Имя - ${nearestEntity.name}, Тип - ${nearestEntity.type}`);
        } else {
            bot.chat(`Не найдено сущностей с именем или типом ${entityType}`);
        }
    }



    else if (parts[0] === "come") {
        targetUsername = parts[1];
        targetPlayer = bot.nearestEntity(entity =>
  (entity.username && entity.username === targetUsername) ||
  (entity.mobType && entity.mobType === targetUsername) ||
  (entity.name && entity.name === targetUsername) ||
  (entity.displayName && entity.displayName === targetUsername) ||
  (entity.entityType && entity.entityType.toString() === targetUsername) ||
  (entity.kind && entity.kind === targetUsername)
);
            if (!targetPlayer) {
                bot.chat(`Не найден моб ${targetUsername}`);
                return;

            }

            playerX = targetPlayer.position.x;
            playerY = targetPlayer.position.y;
            playerZ = targetPlayer.position.z;
            defaultMove = new Movements(bot)
            bot.pathfinder.setMovements(defaultMove)
            bot.pathfinder.setGoal(new GoalNear(playerX, playerY, playerZ, 1))


    }

    else if (parts[0] === "follow") {
        bot.chat("Следую за тобой!");
        following = true;
        bot.pathfinder.setGoal(new goals.GoalFollow(bot.players[username]?.entity, RANGE_GOAL));
    }

    else if (parts[0] === "stop") {
        bot.chat("Останавливаюсь!");
        bot.pvp.stop()
        following = false;
        followingProtectedPlayer = false;  // Останавливаем следование
        protectedPlayer = null;
        bot.pathfinder.setGoal(null); // Сбрасываем цель
        bot.setControlState('forward', false); // Останавливает движение вперед, если оно было
        bot.setControlState('back', false);    // Останавливает движение назад, если оно было
        bot.setControlState('left', false);    // Останавливает движение влево, если оно было
        bot.setControlState('right', false);   // Останавливает движение вправо, если оно было
        bot.setControlState('jump', false);    // Если бот прыгал, останавливает прыжок
        bot.setControlState('sneak', false);   // Если бот приседал, останавливает приседание
    }

});


