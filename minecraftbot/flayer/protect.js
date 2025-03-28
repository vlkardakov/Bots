const mineflayer = require('mineflayer');
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder');
const pvp = require('mineflayer-pvp').plugin;

let protectedPlayer = null;

const bot = mineflayer.createBot({
  host: '87.120.187.59',  // Указал IP сервера
  port: 25565,            // Порт сервера Minecraft
  username: 'Guard'       // Имя бота
});

bot.loadPlugin(pathfinder);
bot.loadPlugin(pvp);

bot.on('chat', (username, message) => {
  // Команда для начала защиты игрока
  if (message.startsWith('protect')) {
    const parts = message.split(' ');
    if (parts.length < 2) {
      bot.chat('Укажи имя игрока для защиты.');
      return;
    }
    protectedPlayer = parts[1];
    bot.chat(`Теперь защищаю игрока ${protectedPlayer}`);
    startProtectingPlayer();
  }

  // Остановка защиты
  if (message === 'stop') {
    bot.chat('Останавливаю защиту.');
    bot.pvp.stop();
    protectedPlayer = null;
    bot.pathfinder.setGoal(null);
  }
});

// Функция для следования за защищаемым игроком
function startProtectingPlayer() {
  if (!protectedPlayer) return;

  const player = bot.players[protectedPlayer];
  if (!player) {
    bot.chat('Не могу найти указанного игрока.');
    return;
  }

  bot.chat(`Следую за игроком ${protectedPlayer}`);
  bot.pathfinder.setGoal(new goals.GoalFollow(player.entity, 1)); // Следуем за игроком на расстоянии 1 блока
}

// Слушаем событие получения урона игроком
bot.on('entityHurt', (entity) => {
  if (protectedPlayer && entity.username === protectedPlayer) {
    // Когда защищаемый игрок получает урон, ищем врага
    bot.chat(`Игрок ${protectedPlayer} получил урон! Ищу врага...`);

    // Ищем ближайшего врага (моба или игрока)
    const targetEnemy = bot.nearestEntity(entity => {
      return (entity.type !== 'other') && entity !== bot.entity && entity.username !== protectedPlayer;
    });

    if (targetEnemy) {
      bot.chat(`Нашел врага: ${targetEnemy.username || targetEnemy.mobType}`);
      bot.pathfinder.setGoal(new goals.GoalFollow(targetEnemy, 1));
      const sword = bot.inventory.items().find(item => item.name.includes("sword"));
      if (sword && (!bot.heldItem || bot.heldItem.type !== sword.type)) {
        bot.equip(sword, 'hand').catch(err => console.log(`Ошибка при экипировке меча: ${err}`));
      }

      bot.pvp.attack(targetEnemy);  // Атакуем врага
    } else {
      bot.chat('Не могу найти врага, чтобы защитить!');
    }
  }
});

// Бот продолжает следовать за игроком, пока он не получит команду `stop`
bot.on('physicTick', () => {
  if (protectedPlayer) {
    const player = bot.players[protectedPlayer];
    if (player) {
      // Если игрок существует, продолжаем следовать за ним
      bot.pathfinder.setGoal(new goals.GoalFollow(player.entity, 1));  // Следуем на 1 блок
    }
  }
});

bot.on('spawn', () => {
  bot.chat('Я готов защищать!');
});
