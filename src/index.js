#!/usr/bin/env node

/**
 * LinkedIn Job Finder Agent - Main Entry Point
 * 
 * This is the main entry point for the LinkedIn job search agent.
 * It provides a CLI interface for searching jobs on LinkedIn.
 * 
 * Usage:
 *   node src/index.js [task-file.json]
 *   node src/index.js --keywords "software engineer" --location "San Francisco"
 */

import { LinkedInJobAgent } from './linkedin-job-agent.js';
import { readFileSync } from 'fs';
import { argv } from 'process';

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = argv.slice(2);
  
  // If first arg is a file path, load it as JSON
  if (args.length === 1 && args[0].endsWith('.json')) {
    try {
      const taskFile = readFileSync(args[0], 'utf-8');
      return JSON.parse(taskFile);
    } catch (error) {
      console.error(`Error reading task file: ${error.message}`);
      process.exit(1);
    }
  }

  // Otherwise, parse command line arguments
  const task = {
    goal: 'Search for jobs on LinkedIn',
    filters: {}
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const value = args[i + 1];

    if (arg === '--keywords' && value) {
      task.filters.keywords = value;
      i++;
    } else if (arg === '--location' && value) {
      task.filters.location = value;
      i++;
    } else if (arg === '--job-type' && value) {
      task.filters.jobType = value;
      i++;
    } else if (arg === '--experience' && value) {
      task.filters.experienceLevel = value;
      i++;
    } else if (arg === '--remote' && value) {
      task.filters.remote = value;
      i++;
    } else if (arg === '--date-posted' && value) {
      task.filters.datePosted = value;
      i++;
    } else if (arg === '--easy-apply') {
      task.filters.easyApply = true;
    } else if (arg === '--company' && value) {
      task.filters.company = value;
      i++;
    } else if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    }
  }

  return task;
}

/**
 * Show help message
 */
function showHelp() {
  console.log(`
LinkedIn Job Finder Agent
=========================

Usage:
  node src/index.js [options]
  node src/index.js task.json

Options:
  --keywords <text>        Job keywords to search for
  --location <text>        Job location (city, state, country)
  --job-type <type>        Job type (full-time, part-time, contract, etc.)
  --experience <level>     Experience level (entry, mid, senior, etc.)
  --remote <type>          Remote type (on-site, remote, hybrid)
  --date-posted <date>     Date posted (today, past week, past month)
  --easy-apply             Filter for Easy Apply jobs only
  --company <name>         Company name
  --help, -h               Show this help message

Examples:
  # Search for software engineering jobs in San Francisco
  node src/index.js --keywords "software engineer" --location "San Francisco, CA"

  # Search for remote senior-level jobs
  node src/index.js --keywords "developer" --remote "remote" --experience "senior"

  # Use a task JSON file
  node src/index.js examples/task.json

Task JSON Format:
  {
    "goal": "Find software engineering jobs",
    "filters": {
      "keywords": "software engineer",
      "location": "San Francisco, CA",
      "jobType": "full-time",
      "experienceLevel": "mid",
      "remote": "hybrid",
      "datePosted": "past week",
      "easyApply": false
    }
  }

Safety Notes:
  - This agent operates only in your logged-in LinkedIn browser
  - It will ask for confirmation before any irreversible actions
  - All actions are logged for transparency
  - Results are stored locally only
  `);
}

/**
 * Main function
 */
async function main() {
  console.log('🤖 LinkedIn Job Finder Agent\n');
  console.log('============================================\n');

  // Parse arguments
  const task = parseArgs();

  // Create agent and run search
  const agent = new LinkedInJobAgent();
  
  try {
    const results = await agent.searchJobs(task);

    if (results.success) {
      console.log('\n============================================');
      console.log('✅ Search completed successfully!');
      console.log(`📊 Found ${results.count} jobs`);
      
      // Export results
      if (results.jobs.length > 0) {
        const filename = await agent.exportResults(results.jobs, 'json');
        console.log(`💾 Results saved to: ${filename}`);
      }

      // Show summary
      console.log('\n📋 Summary:');
      console.log(`   Filters applied: ${Object.keys(results.filters).filter(k => results.filters[k]).length}`);
      console.log(`   Total actions: ${results.actionLog.length}`);
      console.log(`   Completed at: ${results.timestamp}`);
      
    } else {
      console.log('\n============================================');
      console.log('❌ Search failed');
      console.log(`Error: ${results.error}`);
      console.log(`   Partial results: ${results.jobs.length} jobs`);
    }

  } catch (error) {
    console.error('\n❌ Fatal error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run the main function if this is the entry point
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

export { main, parseArgs };
