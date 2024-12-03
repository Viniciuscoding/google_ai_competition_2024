// import { spawn } from 'child_process';

// const test = () => {
//   return new Promise((resolve, reject) => {
//     const pythonProcess = spawn('python', ['./data/python scripts/main.py', 'Node.js']);

//     let output = '';
//     pythonProcess.stdout.on('data', (data) => {
//       output += data.toString();
//     });

//     pythonProcess.stderr.on('data', (data) => {
//       console.error(`Error from Python: ${data.toString()}`);
//       reject(data.toString()); // Reject the promise on error
//     });

//     pythonProcess.on('close', (code) => {
//       if (code === 0) {
//         resolve(output.trim()); // Resolve with the output when process is done
//       } else {
//         reject(`Python process exited with code: ${code}`);
//       }
//     });
//   });
// };

import { PythonShell } from 'python-shell';

const test = async () => {
  return new Promise((resolve, reject) => {
    PythonShell.run('./data/python scripts/main.py', null, (err, messages) => {
      if (err) {
        return reject(err);
      }
      resolve(messages);
    });
  });
};

export default { test };