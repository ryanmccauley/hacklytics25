import { Dialog, DialogContent, DialogTrigger } from "~/components/ui/dialog"

export interface ViewInstructionsDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  instructions: string
  children: React.ReactNode
}

export default (props: ViewInstructionsDialogProps) => {
  return (
    <Dialog
      open={props.open}
      onOpenChange={props.onOpenChange}
    >
      <DialogTrigger asChild>
        {props.children}
      </DialogTrigger>
      <DialogContent>
        Hello world
      </DialogContent>
    </Dialog>
  )
}