import { Router } from 'express';
const router = Router();
import summary from '../data/summary.js';

router.get('/', async(req,res) => {
  try {
    const test = await summary.test();
    return res.status(200).json(test);
  } catch (error) {
    console.error("Error fetching summary:", error);
    return res.status(500).json({ error: "Internal Server Error" });
  }
})

export default router;