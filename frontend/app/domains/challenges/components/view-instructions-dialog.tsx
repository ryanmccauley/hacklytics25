import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTrigger } from "~/components/ui/dialog"
import ReactMarkdown from "react-markdown"
import { Button } from "~/components/ui/button"

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
        <DialogHeader className="font-semibold">
          Challenge Setup Instructions
        </DialogHeader>
        <div className="prose">
          <ReactMarkdown>
            { props.instructions }
          </ReactMarkdown>
        </div>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => props.onOpenChange(false)}
          >
            Close
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}