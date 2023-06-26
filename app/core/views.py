from django.shortcuts import redirect, render
from core.forms import DepositForm
from core.models import Transaction

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.amount import AMOUNT
from user.models import User


def get_user_amount(user):
    acc_bal = 0
    deposiits = Transaction.objects.filter(
        status="approved", tx_type="deposit", creator=user
    )
    transfers_from_account = Transaction.objects.filter(
        status="approved", tx_type="transfer", sender=user
    )
    transfers_to_account = Transaction.objects.filter(
        status="approved", tx_type="transfer", receiver=user
    )

    for tx in deposiits:
        acc_bal += tx.amount
    print(acc_bal, "after deposit")
    for tx in transfers_from_account:
        acc_bal -= tx.amount
    print(acc_bal, "after transfer from")
    for tx in transfers_to_account:
        acc_bal += tx.amount
    print(acc_bal, "after transfer to")

    return acc_bal


@login_required(login_url="/login")
def home_view(request):
    acc_bal = get_user_amount(request.user)

    return render(request, "home.html", {"acc_bal": acc_bal})


@login_required(login_url="/login")
def deposit_view(request):
    form = DepositForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            amount = form.cleaned_data.get("amount")
            description = form.cleaned_data.get("description")

            is_approved = amount < AMOUNT
            Transaction.objects.create(
                creator=request.user,
                tx_type="deposit",
                amount=amount,
                sender=request.user,
                receiver=request.user,
                description=description,
                status="approved" if is_approved else "pending",
            )
            messages.add_message(request, messages.SUCCESS, "Transaction is added.")

            return redirect("transactions")

    return render(request, "deposit.html", {"form": form})


@login_required(login_url="/login")
def transfer_view(request):
    acc_bal = get_user_amount(request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        transfer_to = request.POST.get("transferto")

        print(amount, transfer_to)
        amount = float(amount)
        if amount and transfer_to:
            user_amount = get_user_amount(request.user)
            if amount > user_amount:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "You don't have enough balance to transfer.",
                )
                return redirect("transfer")
            if transfer_to:
                try:
                    reciever = User.objects.get(iban=transfer_to)
                except:
                    messages.add_message(request, messages.ERROR, "Invalid IBAN.")
                    return redirect("transfer")
                Transaction.objects.create(
                    creator=request.user,
                    tx_type="transfer",
                    amount=amount,
                    sender=request.user,
                    receiver=reciever,
                    status="approved" if amount < AMOUNT else "pending",
                )

    return render(request, "transfer.html", {"acc_bal": acc_bal})


@login_required(login_url="/login")
def transactions_view(request):
    transactions = Transaction.objects.all().order_by("-created_at")

    if (
        request.user.is_superuser
        or request.user.is_staff
        or request.user.role == "staff"
    ):
        pass
    else:
        transactions = transactions.filter(creator=request.user) | transactions.filter(
            receiver=request.user
        )

    return render(request, "transactions.html", {"transactions": transactions})


@login_required(login_url="/login")
def approve_view(request, t_id):
    tx = Transaction.objects.get(id=t_id)

    if (
        request.user.is_superuser
        or request.user.is_staff
        or request.user.role == "staff"
    ):
        if tx.tx_type == "deposit":
            tx.status = "approved"
            tx.save()
            messages.add_message(request, messages.SUCCESS, "Transaction is approved.")
            return redirect("transactions")

        elif tx.tx_type == "transfer":
            sender_amount = get_user_amount(tx.sender)
            if sender_amount >= tx.amount:
                tx.status = "approved"
                tx.save()
                messages.add_message(
                    request, messages.SUCCESS, "Transaction is approved."
                )
                return redirect("transactions")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Sender doesn't have enough balance to transfer.",
                )
                return redirect("transactions")

    else:
        messages.add_message(
            request,
            messages.ERROR,
            "You don't have permission to approve this transaction.",
        )

        return redirect("transactions")


@login_required(login_url="/login")
def reject_view(request, t_id):
    tx = Transaction.objects.get(id=t_id)

    if (
        request.user.is_superuser
        or request.user.is_staff
        or request.user.role == "staff"
    ):
        tx.status = "rejected"
        tx.save()
        messages.add_message(request, messages.SUCCESS, "Transaction is approved.")
        return redirect("transactions")

    else:
        messages.add_message(
            request,
            messages.ERROR,
            "You don't have permission to approve this transaction.",
        )

        return redirect("transactions")
