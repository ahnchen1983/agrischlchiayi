#!/usr/bin/env node
import { Command } from 'commander';
import { searchCommand } from './commands/search.js';
import { readCommand } from './commands/read.js';
import { listCommand } from './commands/list.js';
import { randomCommand } from './commands/random.js';
import { syncCommand } from './commands/sync.js';
import { statsCommand } from './commands/stats.js';
import { todayCommand } from './commands/today.js';
import { quizCommand } from './commands/quiz.js';
import { exploreCommand } from './commands/explore.js';
import { diffCommand } from './commands/diff.js';
import { graphCommand } from './commands/graph.js';
import { ragCommand } from './commands/rag.js';
import { contributeCommand } from './commands/contribute.js';
import { validateCommand } from './commands/validate.js';
import { terminologyCommand } from './commands/terminology.js';

const program = new Command();

program
  .name('taiwanmd')
  .description(
    'Taiwan.md — 台灣知識庫 CLI\nSearch, read, and explore 900+ curated articles about Taiwan.',
  )
  .version('0.5.0');

// Register all commands
searchCommand(program);
readCommand(program);
listCommand(program);
randomCommand(program);
syncCommand(program);
statsCommand(program);
todayCommand(program);
quizCommand(program);
exploreCommand(program);
diffCommand(program);
graphCommand(program);
ragCommand(program);
contributeCommand(program);
validateCommand(program);
terminologyCommand(program);

program.parse();
