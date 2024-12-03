import summaryRoutes from './summary.js';

const configRoutes = (app) => {
  // app.use('/', (req, res) => {
  //   res.status(200).json("Hello World!")
  // }); 
  app.use('/summary', summaryRoutes);
  app.use('*', (req, res) => {
    res.status(400).json("Error: Page not found.")
  });
};

export default configRoutes;
